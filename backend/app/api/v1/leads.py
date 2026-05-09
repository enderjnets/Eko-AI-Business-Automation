import logging
import math
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, Body, Request
from sqlalchemy import select, func, Integer, case, and_
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.db.base import get_db, AsyncSessionLocal
from app.models.lead import Lead, LeadStatus, LeadSource, Interaction
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember
from app.models.sequence import EmailSequence, SequenceEnrollment, SequenceStatus
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadPreviewResponse, LeadListResponse, DiscoveryRequest, LeadSearchRequest, PublicLeadCreate
from app.agents.discovery.agent import DiscoveryAgent
from app.agents.research.analyzers.website import WebsiteAnalyzer
from app.agents.research.agent import ResearchAgent
from app.agents.outreach.channels.email import EmailOutreach, EMAIL_TEMPLATES
from app.services.paperclip import on_lead_status_change, on_system_alert
from app.utils.embedding import update_lead_embedding
from app.utils.ai_client import generate_embedding
from app.core.security import get_current_user
from app.services.tenant_context import get_tenant_context_optional, TenantContext
from app.api.v1.crm import VALID_TRANSITIONS
from app.utils.geocoding import geocode_address as _geocode_address

logger = logging.getLogger(__name__)

router = APIRouter()




@router.get("/enrichment-status", response_model=dict)
async def enrichment_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return counts of leads by all statuses."""
    counts = {}
    for s in LeadStatus:
        counts[s.value] = await db.scalar(
            select(func.count()).select_from(Lead).where(Lead.status == s)
        )
    pipeline_total = (
        counts.get(LeadStatus.DISCOVERED.value, 0)
        + counts.get(LeadStatus.ENRICHED.value, 0)
        + counts.get(LeadStatus.SCORED.value, 0)
    )
    return {
        "counts": counts,
        "discovered": counts.get(LeadStatus.DISCOVERED.value, 0),
        "enriched": counts.get(LeadStatus.ENRICHED.value, 0),
        "scored": counts.get(LeadStatus.SCORED.value, 0),
        "total": sum(counts.values()),
        "pipeline_total": pipeline_total,
    }

def _haversine_km(lat1: float, lng1: float, lat2: Optional[float], lng2: Optional[float]) -> Optional[float]:
    """Calculate Haversine distance in km. Returns None if lat2/lng2 are missing."""
    if lat2 is None or lng2 is None:
        return None
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2
    a = min(1.0, max(0.0, a))  # Clamp to protect against floating-point drift
    c = 2 * math.asin(math.sqrt(a))
    return R * c



@router.get("", response_model=LeadListResponse)
async def list_leads(
    status: Optional[LeadStatus] = None,
    city: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=5000),
    lat: Optional[float] = Query(None, description="Reference latitude for distance sorting"),
    lng: Optional[float] = Query(None, description="Reference longitude for distance sorting"),
    sort_by: str = Query("score", enum=["score", "distance", "score_distance"]),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum total score filter"),
    max_score: Optional[float] = Query(None, ge=0, le=100, description="Maximum total score filter"),
    has_email: Optional[bool] = Query(None, description="Filter leads with email"),
    has_phone: Optional[bool] = Query(None, description="Filter leads with phone"),
    has_website: Optional[bool] = Query(None, description="Filter leads with website"),
    category: Optional[str] = Query(None, description="Filter by business category"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List leads with optional filtering, geo-sorting and smart ranking."""
    query = select(Lead)

    # Non-admin users see their own leads + public leads (no owner)
    if not current_user.is_superuser and current_user.role.value != "admin":
        query = query.where(
            (Lead.owner_id == current_user.id) | (Lead.owner_id.is_(None)) | (Lead.assigned_to == current_user.email)
        )

    if status:
        query = query.where(Lead.status == status)
    if city:
        query = query.where(Lead.city.ilike(f"%{city}%"))
    if search:
        query = query.where(Lead.business_name.ilike(f"%{search}%"))
    if category:
        query = query.where(Lead.category.ilike(f"%{category}%"))
    if min_score is not None:
        query = query.where(func.coalesce(Lead.total_score, 0) >= min_score)
    if max_score is not None:
        query = query.where(func.coalesce(Lead.total_score, 0) <= max_score)
    if has_email is True:
        query = query.where(Lead.email.isnot(None) & (Lead.email != ''))
    elif has_email is False:
        query = query.where((Lead.email.is_(None)) | (Lead.email == ''))
    if has_phone is True:
        query = query.where(Lead.phone.isnot(None) & (Lead.phone != ''))
    elif has_phone is False:
        query = query.where((Lead.phone.is_(None)) | (Lead.phone == ''))
    if has_website is True:
        query = query.where(Lead.website.isnot(None) & (Lead.website != ''))
    elif has_website is False:
        query = query.where((Lead.website.is_(None)) | (Lead.website == ''))

    # Count total before pagination / sorting
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Contactability score expression (reused for geo and non-geo sorts)
    contact_score = (
        func.coalesce(func.nullif(Lead.email, '').isnot(None).cast(Integer), 0) +
        func.coalesce(func.nullif(Lead.phone, '').isnot(None).cast(Integer), 0) +
        case(
            (Lead.website.isnot(None) & (Lead.website != '') & ~Lead.website.ilike('%yelp.com%'), 1),
            else_=0
        )
    )

    # Geo-sorting: use SQL-side Haversine distance for deterministic, scalable ordering
    needs_geo_sort = lat is not None and lng is not None and sort_by in ("distance", "score_distance")
    if needs_geo_sort:
        lat_rad = func.radians(lat)
        lng_rad = func.radians(lng)
        lead_lat_rad = func.radians(Lead.latitude)
        lead_lng_rad = func.radians(Lead.longitude)
        dlat = lead_lat_rad - lat_rad
        dlng = lead_lng_rad - lng_rad
        a = (
            func.pow(func.sin(dlat / 2), 2) +
            func.cos(lat_rad) * func.cos(lead_lat_rad) * func.pow(func.sin(dlng / 2), 2)
        )
        c = 2 * func.asin(func.sqrt(func.least(1.0, func.greatest(0.0, a))))
        distance_expr = (6371.0 * c).label("distance_km")

        # Only leads with coordinates can be distance-sorted
        query = query.where(Lead.latitude.isnot(None) & Lead.longitude.isnot(None))

        if sort_by == "distance":
            query = query.order_by(distance_expr.asc())
        elif sort_by == "score_distance":
            query = query.order_by(
                contact_score.desc(),
                func.coalesce(Lead.total_score, 0).desc(),
                distance_expr.asc(),
            )

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        leads = list(result.scalars().all())

        # Compute distance_km on the small paginated result set for serialization
        for lead in leads:
            lead.distance_km = _haversine_km(lat, lng, lead.latitude, lead.longitude)

        return LeadListResponse(
            total=total,
            items=leads,
            page=page,
            page_size=page_size,
        )

    # Standard SQL-side sorting (no geo reference)
    if sort_by == "score":
        query = query.order_by(contact_score.desc(), func.coalesce(Lead.total_score, 0).desc(), Lead.created_at.desc())
    elif sort_by == "score_distance" and (lat is None or lng is None):
        # Fallback to score-only if lat/lng missing
        query = query.order_by(contact_score.desc(), func.coalesce(Lead.total_score, 0).desc(), Lead.created_at.desc())
    else:
        query = query.order_by(Lead.created_at.desc())

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    leads = result.scalars().all()

    # Calculate distance_km for all leads with coordinates when lat/lng provided
    if lat is not None and lng is not None:
        for lead in leads:
            lead.distance_km = _haversine_km(lat, lng, lead.latitude, lead.longitude)

    return LeadListResponse(
        total=total,
        items=leads,
        page=page,
        page_size=page_size,
    )


@router.get("/autocomplete/names", response_model=list[str])
async def autocomplete_lead_names(
    q: str = Query(..., min_length=1, description="Search prefix"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: TenantContext = Depends(get_tenant_context_optional),
):
    """Return matching business names for autocomplete."""
    query = (
        select(Lead.business_name)
        .where(Lead.business_name.ilike(f"%{q}%"))
        .distinct()
        .limit(limit)
    )
    # Apply workspace filter (RLS-compatible)
    if tenant.workspace_id:
        query = query.where(Lead.workspace_id == tenant.workspace_id)
    else:
        # Fallback: non-admin users only see their own leads
        if not current_user.is_superuser and current_user.role.value != "admin":
            query = query.where(
                (Lead.owner_id == current_user.id) | (Lead.assigned_to == current_user.email)
            )

    result = await db.execute(query)
    return list(result.scalars().all())


def _check_lead_access(lead: Lead, current_user: User):
    """Raise 403 if the user is not authorized to access this lead.
    Admins/superusers can access any lead. Users can access leads they own
    or that are assigned to them. Public leads (owner_id is None) are visible
    to all authenticated users.
    """
    if current_user.is_superuser or current_user.role.value == "admin":
        return
    if lead.owner_id is None:
        return
    if lead.owner_id == current_user.id:
        return
    if lead.assigned_to and lead.assigned_to == current_user.email:
        return
    raise HTTPException(status_code=403, detail="Not authorized to access this lead")


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single lead by ID."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    _check_lead_access(lead, current_user)
    return lead


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(
    lead_data: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant: TenantContext = Depends(get_tenant_context_optional),
):
    """Create a new lead manually. Auto-runs enrichment and initial outreach."""
    data = lead_data.model_dump()
    workspace_id = data.get("workspace_id") or tenant.workspace_id
    if not workspace_id and current_user:
        result = await db.execute(
            select(WorkspaceMember)
            .where(WorkspaceMember.user_id == current_user.id)
            .order_by(WorkspaceMember.created_at)
            .limit(1)
        )
        member = result.scalar_one_or_none()
        if member:
            workspace_id = member.workspace_id
    data["workspace_id"] = workspace_id

    # Check for duplicates by business_name or email
    dup_query = select(Lead).where(
        (Lead.workspace_id == workspace_id) &
        (
            (Lead.business_name.ilike(lead_data.business_name.strip())) |
            (lead_data.email is not None and Lead.email == lead_data.email)
        )
    ).limit(1)
    dup_result = await db.execute(dup_query)
    existing = dup_result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Lead already exists: {existing.business_name} (ID: {existing.id})",
        )

    # Geocode address BEFORE creating the lead so coords are included in the response
    if data.get("latitude") is None and data.get("longitude") is None:
        geo = await _geocode_address(
            address=lead_data.address or "",
            city=lead_data.city or "",
            state=lead_data.state or "",
            zip_code=lead_data.zip_code or "",
        )
        if geo:
            data["latitude"] = geo["lat"]
            data["longitude"] = geo["lng"]
            logger.info(f"Geocoded address to {geo['lat']}, {geo['lng']}")

    lead = Lead(**data, owner_id=current_user.id)
    db.add(lead)
    await db.commit()
    await db.refresh(lead)

    # Generate embedding for semantic search
    try:
        embed_text = f"{lead.business_name} {lead.category or ''} {lead.address or ''} {lead.city or ''} {lead.state or ''} {lead.zip_code or ''}".strip()
        if embed_text:
            lead.embedding = await generate_embedding(embed_text)
            await db.commit()
            logger.info(f"Generated embedding for lead {lead.id}")
    except Exception as e:
        logger.warning(f"Failed to generate embedding for lead {lead.id}: {e}")

    # Queue background pipeline (enrichment + initial outreach)
    try:
        from app.tasks.scheduled import run_lead_pipeline
        run_lead_pipeline.delay(lead.id)
        logger.info(f"Queued lead pipeline for lead {lead.id}")
    except Exception as e:
        logger.warning(f"Failed to queue lead pipeline for lead {lead.id}: {e}")

    return lead




@router.post("/preview", response_model=LeadPreviewResponse)
async def preview_lead(
    lead_data: LeadCreate,
    current_user: User = Depends(get_current_user),
):
    """Preview lead creation: extract website data and compare with manual input."""
    from app.schemas.lead import FieldDiscrepancy, LeadPreviewResponse

    manual = {
        "business_name": lead_data.business_name or "",
        "email": lead_data.email or "",
        "category": lead_data.category or "",
        "phone": lead_data.phone or "",
        "address": lead_data.address or "",
        "city": lead_data.city or "",
        "state": lead_data.state or "",
        "zip_code": lead_data.zip_code or "",
    }

    extracted = {
        "business_name": "",
        "email": "",
        "category": "",
        "phone": "",
        "address": "",
        "city": "",
        "state": "",
        "zip_code": "",
    }

    website = lead_data.website
    if website:
        analyzer = WebsiteAnalyzer()
        try:
            data = await analyzer.analyze(website)
            # business_name from title or schema.org
            extracted["business_name"] = data.get("business_name_found") or _clean_website_title(data.get("title", ""))
            extracted["email"] = data.get("email_found") or ""
            extracted["phone"] = data.get("phone_found") or ""
            extracted["address"] = data.get("address_found") or ""
            extracted["city"] = data.get("city_found") or ""
            extracted["state"] = data.get("state_found") or ""
            extracted["zip_code"] = data.get("zip_found") or ""
            # category from first service or title keywords
            services = data.get("services", [])
            if services:
                extracted["category"] = services[0]
        except Exception as e:
            logger.warning(f"Website analysis failed for preview: {e}")
        finally:
            try:
                await analyzer.close()
            except Exception:
                pass

    # Build discrepancies list
    discrepancies = []
    field_labels = {
        "business_name": "Nombre del negocio",
        "email": "Email",
        "category": "Categoría",
        "phone": "Teléfono",
        "address": "Dirección",
        "city": "Ciudad",
        "state": "Estado",
        "zip_code": "Código Postal",
    }

    import re as _re

    for field, label in field_labels.items():
        m_val = (manual.get(field) or "").strip()
        e_val = (extracted.get(field) or "").strip()
        if not m_val and not e_val:
            continue
        # Normalize phone for comparison (digits only)
        if field == "phone" and m_val and e_val:
            m_digits = _re.sub(r"\D", "", m_val)
            e_digits = _re.sub(r"\D", "", e_val)
            if m_digits == e_digits:
                continue
        if e_val and m_val.lower() != e_val.lower():
            discrepancies.append(
                FieldDiscrepancy(
                    field=field,
                    label=label,
                    manual_value=m_val or None,
                    extracted_value=e_val or None,
                )
            )
        elif m_val and not e_val:
            # Web page does not have this data — warn user
            discrepancies.append(
                FieldDiscrepancy(
                    field=field,
                    label=label,
                    manual_value=m_val or None,
                    extracted_value=None,
                )
            )

    return LeadPreviewResponse(
        manual=manual,
        extracted=extracted,
        discrepancies=discrepancies,
        has_discrepancies=len(discrepancies) > 0,
    )


def _clean_website_title(title: str) -> str:
    """Clean website title to extract business name."""
    if not title:
        return ""
    # Remove common separators and suffixes
    for sep in [" | ", " - ", " – ", " — ", " |", " -", " :: ", " : "]:
        if sep in title:
            title = title.split(sep)[0]
            break
    return title.strip()


async def _send_welcome_email(lead_id: int):
    """Background task: send the Free AI Analysis welcome email immediately."""
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Lead).where(Lead.id == lead_id))
            lead = result.scalar_one_or_none()
            if not lead or not lead.email:
                logger.warning(f"Cannot send welcome email: lead {lead_id} not found or no email")
                return

            outreach = EmailOutreach()
            await outreach.generate_and_send(
                lead=lead,
                template_key="nurture_welcome",
            )
            logger.info(f"Welcome email sent to lead {lead_id} ({lead.email})")
    except Exception as e:
        logger.error(f"Failed to send welcome email to lead {lead_id}: {e}")


@router.post("/public", response_model=dict, status_code=201)
async def create_public_lead(
    lead_data: PublicLeadCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Create a new lead from the public marketing website (no auth required)."""
    # Check for duplicate by email
    if lead_data.email:
        result = await db.execute(select(Lead).where(Lead.email == lead_data.email))
        existing = result.scalar_one_or_none()
        if existing:
            return {"status": "existing", "lead_id": existing.id, "message": "Lead already exists"}

    lead = Lead(
        business_name=lead_data.business_name,
        email=lead_data.email,
        phone=lead_data.phone,
        category=lead_data.category,
        source=LeadSource.MANUAL,
        status=LeadStatus.DISCOVERED,
        notes=lead_data.notes or "Captured from public landing page",
        source_data={
            "origin": "website_landing",
            "captured_at": datetime.utcnow().isoformat(),
            "first_name": lead_data.first_name,
            "last_name": lead_data.last_name,
        },
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)

    # Record interaction
    interaction = Interaction(
        lead_id=lead.id,
        interaction_type="note",
        direction="inbound",
        subject="Lead captured from website",
        content=lead_data.notes or "Lead submitted via public landing page form",
        meta={"source": "website_landing", "category": lead_data.category},
    )
    db.add(interaction)
    await db.commit()

    # Auto-enroll in nurture sequence (only if lead has email)
    if lead.email:
        try:
            seq_result = await db.execute(
                select(EmailSequence).where(EmailSequence.name == "Landing Page Nurturing")
            )
            seq = seq_result.scalar_one_or_none()
            if seq and seq.status == SequenceStatus.ACTIVE:
                # Check not already enrolled
                existing_enr = await db.execute(
                    select(SequenceEnrollment).where(
                        SequenceEnrollment.sequence_id == seq.id,
                        SequenceEnrollment.lead_id == lead.id,
                        SequenceEnrollment.status.in_(["active", "paused"]),
                    )
                )
                if not existing_enr.scalar_one_or_none():
                    enrollment = SequenceEnrollment(
                        sequence_id=seq.id,
                        lead_id=lead.id,
                        status="active",
                        current_step_position=0,
                        next_step_at=datetime.utcnow(),
                        meta={"source": "website_landing_auto_enroll"},
                    )
                    db.add(enrollment)
                    seq.leads_entered += 1
                    await db.commit()
                    logger.info(f"Auto-enrolled lead {lead.id} in nurture sequence {seq.id}")
        except Exception as e:
            logger.warning(f"Failed to auto-enroll lead {lead.id} in nurture sequence: {e}")
    else:
        logger.info(f"Lead {lead.id} has no email, skipping nurture enrollment")

    # Send welcome email immediately in background
    if lead.email:
        background_tasks.add_task(_send_welcome_email, lead.id)

    return {"status": "created", "lead_id": lead.id}


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    _check_lead_access(lead, current_user)

    update_data = lead_update.model_dump(exclude_unset=True)

    # Validate status transitions if status is being updated
    if "status" in update_data:
        new_status = update_data["status"]
        if isinstance(new_status, str):
            new_status = LeadStatus(new_status)
        allowed = VALID_TRANSITIONS.get(lead.status, [])
        if new_status not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition from {lead.status.value} to {new_status.value}. Allowed: {[s.value for s in allowed]}"
            )
        # Record the transition as an interaction
        old_status = lead.status.value
        interaction = Interaction(
            lead_id=lead.id,
            interaction_type="note",
            direction="outbound",
            content=f"Status changed from {old_status} to {new_status.value}",
            meta={"transition": True, "from": old_status, "to": new_status.value, "source": "api_patch"},
        )
        db.add(interaction)

    # Whitelist allowed fields to prevent accidental dynamic attribute creation
    allowed_fields = {c.name for c in Lead.__table__.columns}
    for field, value in update_data.items():
        if field in allowed_fields:
            setattr(lead, field, value)

    await db.commit()
    await db.refresh(lead)
    return lead


@router.delete("/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    _check_lead_access(lead, current_user)

    await db.delete(lead)
    await db.commit()
    return None


@router.post("/{lead_id}/enrich", response_model=LeadResponse)
async def enrich_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Run research agent to enrich a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    _check_lead_access(lead, current_user)

    research_agent = ResearchAgent()
    enriched = await research_agent.enrich(lead)
    
    # Update lead with enriched data
    for field, value in enriched.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    
    old_status = lead.status.value
    if lead.urgency_score is not None and lead.fit_score is not None:
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
    request: DiscoveryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Run discovery agent to find new leads."""
    agent = DiscoveryAgent()
    leads_data = await agent.discover(
        query=request.query,
        city=request.city,
        state=request.state,
        radius_miles=request.radius_miles,
        max_results=request.max_results,
        sources=request.sources,
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
        
        lead = Lead(**lead_data, owner_id=current_user.id)
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
    
    return {
        "total": len(created_leads),
        "page": 1,
        "page_size": len(created_leads),
        "items": created_leads,
    }


@router.post("/search", response_model=LeadListResponse)
async def search_leads(
    request: LeadSearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    search_term = request.query.strip().lower()

    # 1. Try exact name match first
    exact_query = select(Lead).where(Lead.business_name.ilike(f"%{search_term}%"))
    if not current_user.is_superuser and current_user.role.value != "admin":
        exact_query = exact_query.where(
            (Lead.owner_id == current_user.id) | (Lead.assigned_to == current_user.email) | (Lead.owner_id.is_(None))
        )
    if request.status:
        exact_query = exact_query.where(Lead.status == request.status)
    if request.min_score is not None:
        exact_query = exact_query.where(Lead.total_score >= request.min_score)
    exact_query = exact_query.limit(request.limit)

    exact_result = await db.execute(exact_query)
    exact_items = exact_result.scalars().all()
    if exact_items:
        return LeadListResponse(
            total=len(exact_items),
            items=list(exact_items),
            page=1,
            page_size=len(exact_items),
        )

    # 2. Fallback to semantic search via embeddings
    distance_expr = Lead.embedding.op("<=>")(query_embedding)
    semantic_query = (
        select(Lead)
        .where(Lead.embedding.isnot(None))
        .where(distance_expr < 0.5)
        .order_by(distance_expr)
        .limit(request.limit)
    )
    if not current_user.is_superuser and current_user.role.value != "admin":
        semantic_query = semantic_query.where(
            (Lead.owner_id == current_user.id) | (Lead.assigned_to == current_user.email) | (Lead.owner_id.is_(None))
        )
    if request.status:
        semantic_query = semantic_query.where(Lead.status == request.status)
    if request.min_score is not None:
        semantic_query = semantic_query.where(Lead.total_score >= request.min_score)

    semantic_result = await db.execute(semantic_query)
    semantic_items = semantic_result.scalars().all()

    return LeadListResponse(
        total=len(semantic_items),
        items=list(semantic_items),
        page=1,
        page_size=len(semantic_items),
    )


@router.post("/enrich-all", response_model=dict)
async def enrich_all_leads(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Enqueue enrichment for all discovered/enriched leads without a real website analyzed."""
    query = select(Lead.id).where(
        Lead.status.in_([LeadStatus.DISCOVERED, LeadStatus.ENRICHED])
    )
    # Ownership filter
    if not current_user.is_superuser and current_user.role.value != "admin":
        query = query.where(
            (Lead.owner_id == current_user.id) | (Lead.assigned_to == current_user.email) | (Lead.owner_id.is_(None))
        )
    result = await db.execute(query)
    lead_ids = [row[0] for row in result.all()]

    # Run in background so the HTTP request returns immediately
    # Pass only IDs — the background task opens its own fresh session
    background_tasks.add_task(_enrich_leads_batch, lead_ids)

    return {
        "message": f"Enrichment started for {len(lead_ids)} leads in the background",
        "total": len(lead_ids),
    }


async def _enrich_leads_batch(lead_ids: list[int]):
    """Background task: enrich a batch of leads. Opens its own DB session."""
    from app.db.base import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        agent = ResearchAgent()
        enriched_count = 0
        failed_count = 0

        for lead_id in lead_ids:
            try:
                result = await db.execute(select(Lead).where(Lead.id == lead_id))
                lead = result.scalar_one_or_none()
                if not lead:
                    continue

                enriched = await agent.enrich(lead)
                for field, value in enriched.model_dump(exclude_unset=True).items():
                    setattr(lead, field, value)

                if lead.urgency_score is not None and lead.fit_score is not None:
                    lead.total_score = (lead.urgency_score + lead.fit_score) / 2
                    lead.status = LeadStatus.SCORED
                else:
                    lead.status = LeadStatus.ENRICHED

                # Update embedding
                try:
                    await update_lead_embedding(lead)
                except Exception:
                    pass

                enriched_count += 1
            except Exception as e:
                logger.error(f"Failed to enrich lead {lead_id}: {e}")
                failed_count += 1

        await db.commit()
    logger.info(f"Batch enrichment complete: {enriched_count} enriched, {failed_count} failed")


@router.post("/bulk/contact", response_model=dict)
async def bulk_contact_leads(
    lead_ids: List[int] = Body(..., description="List of lead IDs to contact"),
    template: str = Body("initial_outreach", description="Email template key to use"),
    custom_subject: Optional[str] = Body(None, description="Optional custom subject (overrides AI generation)"),
    custom_body: Optional[str] = Body(None, description="Optional custom body (overrides AI generation)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Bulk contact multiple leads via email.
    Only contacts leads in SCORED status with email and do_not_contact=False.
    Rate limited to MAX_CAMPAIGN_EMAILS_PER_BATCH (50) per request.
    """
    from app.api.v1.campaigns import MAX_CAMPAIGN_EMAILS_PER_BATCH

    if len(lead_ids) > MAX_CAMPAIGN_EMAILS_PER_BATCH:
        raise HTTPException(
            status_code=400,
            detail=f"Max {MAX_CAMPAIGN_EMAILS_PER_BATCH} leads per bulk contact request"
        )
    
    if template not in EMAIL_TEMPLATES:
        template = "initial_outreach"
    
    # Fetch eligible leads
    result = await db.execute(
        select(Lead).where(
            and_(
                Lead.id.in_(lead_ids),
                Lead.status == LeadStatus.SCORED,
                Lead.email.isnot(None),
                Lead.do_not_contact == False,
            )
        )
    )
    leads = result.scalars().all()
    
    if not leads:
        raise HTTPException(
            status_code=400,
            detail="No eligible leads found. Need leads in SCORED status with email."
        )
    
    email_outreach = EmailOutreach()
    sent_count = 0
    failed_count = 0
    results = []
    
    for lead in leads:
        try:
            if custom_subject and custom_body:
                # Manual email
                response = await email_outreach.send(
                    to_email=lead.email,
                    subject=custom_subject,
                    body=custom_body,
                    lead_id=lead.id,
                    business_name=lead.business_name,
                    ai_generated=False,
                )
            else:
                # AI-generated email
                response = await email_outreach.generate_and_send(
                    lead=lead,
                    template_key=template,
                )
            
            # Record interaction
            interaction = Interaction(
                lead_id=lead.id,
                interaction_type="email",
                direction="outbound",
                subject=response.get("subject", custom_subject or ""),
                content=response.get("body", custom_body or ""),
                email_status="sent",
                email_message_id=response.get("id"),
                meta={
                    "template": template,
                    "ai_generated": not (custom_subject and custom_body),
                    "bulk_contact": True,
                },
            )
            db.add(interaction)
            
            # Update lead status
            lead.status = LeadStatus.CONTACTED
            lead.last_contact_at = datetime.utcnow()
            
            sent_count += 1
            results.append({"lead_id": lead.id, "status": "sent", "message_id": response.get("id")})
            
        except Exception as e:
            failed_count += 1
            logger.error(f"Bulk contact failed for lead {lead.id}: {e}")
            results.append({"lead_id": lead.id, "status": "failed", "error": str(e)})
            
            # Record failed interaction
            interaction = Interaction(
                lead_id=lead.id,
                interaction_type="email",
                direction="outbound",
                content=f"Bulk contact FAILED: {str(e)}",
                email_status="bounced",
                meta={"template": template, "bulk_contact": True, "error": str(e)},
            )
            db.add(interaction)
    
    await db.commit()
    
    return {
        "total_requested": len(lead_ids),
        "eligible": len(leads),
        "sent": sent_count,
        "failed": failed_count,
        "results": results,
    }
