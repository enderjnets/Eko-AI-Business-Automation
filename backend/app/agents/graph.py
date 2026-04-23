"""
LangGraph State Machine for Lead Lifecycle Management.

This defines the multi-agent workflow that orchestrates the entire
sales process from discovery to close.
"""

from typing import TypedDict, Annotated, Optional, List
import operator

from langgraph.graph import StateGraph, END


class LeadState(TypedDict):
    """Shared state across the agent graph."""
    lead_id: int
    business_name: str
    current_status: str
    urgency_score: Optional[float]
    fit_score: Optional[float]
    total_score: Optional[float]
    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    pain_points: List[str]
    trigger_events: List[str]
    interactions_count: int
    last_contact_type: Optional[str]
    next_action: Optional[str]
    error: Optional[str]


# ============ NODE FUNCTIONS ============

def discovery_node(state: LeadState) -> LeadState:
    """Discovery agent: find and validate lead."""
    # This is triggered externally via API; the graph handles transitions
    state["current_status"] = "discovered"
    return state


def research_node(state: LeadState) -> LeadState:
    """Research agent: enrich lead data."""
    if state["current_status"] not in ["discovered", "enriched"]:
        state["error"] = "Cannot research: invalid status"
        return state
    
    state["current_status"] = "enriched"
    return state


def scoring_node(state: LeadState) -> LeadState:
    """Scoring engine: calculate urgency and fit."""
    if state["current_status"] != "enriched":
        state["error"] = "Cannot score: lead not enriched"
        return state
    
    # Calculate composite score
    urgency = state.get("urgency_score") or 0
    fit = state.get("fit_score") or 0
    state["total_score"] = (urgency + fit) / 2
    state["current_status"] = "scored"
    return state


def outreach_node(state: LeadState) -> LeadState:
    """Outreach agent: initiate contact."""
    if state["current_status"] != "scored":
        state["error"] = "Cannot outreach: lead not scored"
        return state
    
    # Determine best channel based on available data
    if state.get("email"):
        state["last_contact_type"] = "email"
    elif state.get("phone"):
        state["last_contact_type"] = "voice"
    else:
        state["error"] = "No contact method available"
        return state
    
    state["interactions_count"] = state.get("interactions_count", 0) + 1
    state["current_status"] = "contacted"
    return state


def engagement_node(state: LeadState) -> LeadState:
    """CRM agent: handle engagement and follow-ups."""
    if state["current_status"] != "contacted":
        state["error"] = "Invalid transition to engaged"
        return state
    
    state["current_status"] = "engaged"
    state["next_action"] = "schedule_meeting"
    return state


def meeting_node(state: LeadState) -> LeadState:
    """Calendar agent: book meetings."""
    if state["current_status"] != "engaged":
        state["error"] = "Cannot book meeting: not engaged"
        return state
    
    state["current_status"] = "meeting_booked"
    state["next_action"] = "send_proposal"
    return state


def proposal_node(state: LeadState) -> LeadState:
    """Sales agent: send proposal."""
    if state["current_status"] != "meeting_booked":
        state["error"] = "Cannot send proposal: meeting not booked"
        return state
    
    state["current_status"] = "proposal_sent"
    state["next_action"] = "follow_up"
    return state


def close_won_node(state: LeadState) -> LeadState:
    """Close won: transition to customer success."""
    state["current_status"] = "closed_won"
    state["next_action"] = "onboarding"
    return state


def close_lost_node(state: LeadState) -> LeadState:
    """Close lost: schedule reactivation."""
    state["current_status"] = "closed_lost"
    state["next_action"] = "reactivate_in_90_days"
    return state


# ============ CONDITIONAL EDGES ============

def should_outreach(state: LeadState) -> str:
    """Decide if lead is worth outreach based on score."""
    score = state.get("total_score") or 0
    if score >= 50:
        return "outreach"
    return "nurture"


def after_contact(state: LeadState) -> str:
    """Determine next step after contact."""
    if state.get("error"):
        return "error"
    # In reality, this would check for response
    return "wait_for_response"


# ============ BUILD GRAPH ============

def build_lead_graph() -> StateGraph:
    """Build and return the lead lifecycle state graph."""
    
    workflow = StateGraph(LeadState)
    
    # Add nodes
    workflow.add_node("discovery", discovery_node)
    workflow.add_node("research", research_node)
    workflow.add_node("scoring", scoring_node)
    workflow.add_node("outreach", outreach_node)
    workflow.add_node("engagement", engagement_node)
    workflow.add_node("meeting", meeting_node)
    workflow.add_node("proposal", proposal_node)
    workflow.add_node("close_won", close_won_node)
    workflow.add_node("close_lost", close_lost_node)
    
    # Add edges
    workflow.set_entry_point("discovery")
    workflow.add_edge("discovery", "research")
    workflow.add_edge("research", "scoring")
    
    # Conditional from scoring
    workflow.add_conditional_edges(
        "scoring",
        should_outreach,
        {
            "outreach": "outreach",
            "nurture": END,  # Low score leads end here for now
        }
    )
    
    workflow.add_edge("outreach", "engagement")
    workflow.add_edge("engagement", "meeting")
    workflow.add_edge("meeting", "proposal")
    
    # From proposal, can go to won or lost
    workflow.add_conditional_edges(
        "proposal",
        lambda s: "won" if s.get("current_status") == "proposal_sent" else "lost",
        {
            "won": "close_won",
            "lost": "close_lost",
        }
    )
    
    workflow.add_edge("close_won", END)
    workflow.add_edge("close_lost", END)
    
    return workflow.compile()


# Global compiled graph instance
lead_graph = build_lead_graph()
