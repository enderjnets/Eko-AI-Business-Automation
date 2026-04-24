from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadListResponse, DiscoveryRequest, LeadSearchRequest
from app.agents.discovery.agent import DiscoveryAgent
from app.agents.research.agent import ResearchAgent
from app.services.paperclip import on_lead_status_change, on_system_alert
from app.utils.embedding import update_lead_embedding
from app.utils.ai_client import generate_embedding

router = APIRouter()


@router.get("", response_model=LeadListResponse)
async def list_leads(
    status: Optional[LeadStatus] = None,
    city: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List leads with optional filtering."""
    query = select(Lead)
    
    if status:
        query = query.where(Lead.status == status)
    if city:
        query = query.where(Lead.city.ilike(f"%{city}%"))
    if search:
        query = query.where(Lead.business_name.ilike(f"%{search}%"))
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Pagination
    query = query.order_by(Lead.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    leads = result.scalars().all()
    
    return LeadListResponse(
        total=total or 0,
        items=leads,
        page=page,
        page_size=page_size,
    )


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single lead by ID."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(lead_data: LeadCreate, db: AsyncSession = Depends(get_db)):
    """Create a new lead manually."""
    lead = Lead(**lead_data.model_dump())
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int, lead_update: LeadUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    for field, value in lead_update.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    
    await db.commit()
    await db.refresh(lead)
    return lead


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    await db.delete(lead)
    await db.commit()
    return None


@router.post("/{lead_id}/enrich", response_model=LeadResponse)
async def enrich_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    """Run research agent to enrich a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    research_agent = ResearchAgent()
    enriched = await research_agent.enrich(lead)
    
    # Update lead with enriched data
    for field, value in enriched.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    
    old_status = lead.status.value
    if lead.urgency_score and lead.fit_score:
        lead.total_score = (lead.urgency_score + lead.fit_score) / 2
        lead.status = LeadStatus.SCORED
    else:
        lead.status = LeadStatus.ENRICHED
    
    await db.commit()
    await db.refresh(lead)
    
    # Generate updated embedding with enriched data
    try:
        await update_lead_embedding(lead)
        await db.commit()
    except Exception:
        pass
    
    # Paperclip: log status change
    try:
        on_lead_status_change(
            lead_id=lead.id,
            business_name=lead.business_name,
            old_status=old_status,
            new_status=lead.status.value,
        )
    except Exception:
        pass
    
    return lead


@router.post("/discover", response_model=LeadListResponse, status_code=201)
async def discover_leads(
    request: DiscoveryRequest, db: AsyncSession = Depends(get_db)
):
    """Run discovery agent to find new leads."""
    agent = DiscoveryAgent()
    leads_data = await agent.discover(
        query=request.query,
        city=request.city,
        state=request.state,
        radius_miles=request.radius_miles,
        max_results=request.max_results,
    )
    
    created_leads = []
    for lead_data in leads_data:
        # Check for duplicates by business_name + city
        existing = await db.execute(
            select(Lead).where(
                Lead.business_name == lead_data["business_name"],
                Lead.city == lead_data.get("city"),
            )
        )
        if existing.scalar_one_or_none():
            continue
        
        lead = Lead(**lead_data)
        if request.campaign_id:
            lead.source_data = {"campaign_id": request.campaign_id}
        db.add(lead)
        created_leads.append(lead)
    
    await db.commit()
    for lead in created_leads:
        await db.refresh(lead)
        # Generate embedding for semantic search (non-blocking to response)
        try:
            await update_lead_embedding(lead)
        except Exception:
            pass
    
    # Save embeddings
    if created_leads:
        await db.commit()
    
    return LeadListResponse(
        total=len(created_leads),
        items=created_leads,
        page=1,
        page_size=len(created_leads),
    )


@router.post("/search", response_model=LeadListResponse)
async def search_leads(
    request: LeadSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """Semantic search over leads using vector similarity."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query is required")

    # Generate embedding for the search query
    try:
        query_embedding = await generate_embedding(request.query)
    except Exception as e:
        logger.error(f"Failed to generate query embedding: {e}")
        raise HTTPException(status_code=500, detail="Embedding generation failed")

    # Build query with cosine distance using pgvector
    distance_expr = Lead.embedding.op("<=>")(query_embedding)
    query = (
        select(Lead, distance_expr.label("distance"))
        .where(Lead.embedding.isnot(None))
        .order_by(distance_expr)
        .limit(request.limit)
    )

    if request.status:
        query = query.where(Lead.status == request.status)
    if request.min_score is not None:
        query = query.where(Lead.total_score >= request.min_score)

    result = await db.execute(query)
    rows = result.all()

    # Filter by similarity threshold (cosine distance < 0.5 means fairly similar)
    items = []
    for lead, distance in rows:
        if distance < 0.5:
            items.append(lead)

    return LeadListResponse(
        total=len(items),
        items=items,
        page=1,
        page_size=len(items),
    )
