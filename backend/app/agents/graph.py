"""
LangGraph State Machine for Generic Object Lifecycle Management.

This defines a metadata-aware multi-agent workflow that can orchestrate
any object type registered in the metadata engine.
"""

from typing import TypedDict, Annotated, Optional, List, Any
import operator

from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """Shared state across the agent graph — metadata-aware and generic."""
    # Identity
    record_id: Optional[str]
    object_name: str              # e.g. "lead", "deal", "property"
    workspace_id: Optional[str]
    label: str

    # Core data (schema-validated at runtime via metadata engine)
    data: dict                    # JSONB payload from DynamicRecord

    # Pipeline status
    current_status: str
    previous_status: Optional[str]

    # Scoring (generic — applicable to any object with score fields)
    score_fields: dict            # {field_name: value} e.g. {"urgency_score": 75, "fit_score": 60}
    total_score: Optional[float]

    # Contact / outreach
    contact_channels: List[str]   # Available channels: email, phone, sms, voice
    last_contact_type: Optional[str]
    interactions_count: int

    # Next action / scheduling
    next_action: Optional[str]
    next_action_due: Optional[str]  # ISO datetime

    # Processing flags
    error: Optional[str]
    enriched: bool
    discovered: bool


# ============ NODE FUNCTIONS ============

def discovery_node(state: AgentState) -> AgentState:
    """Discovery agent: find and validate record."""
    state["current_status"] = "discovered"
    state["discovered"] = True
    state["interactions_count"] = 0
    return state


def research_node(state: AgentState) -> AgentState:
    """Research agent: enrich record data."""
    if state["current_status"] not in ["discovered", "enriched"]:
        state["error"] = "Cannot research: invalid status"
        return state
    state["current_status"] = "enriched"
    state["enriched"] = True
    return state


def scoring_node(state: AgentState) -> AgentState:
    """Scoring engine: calculate composite score from score_fields."""
    if state["current_status"] != "enriched":
        state["error"] = "Cannot score: record not enriched"
        return state

    scores = state.get("score_fields") or {}
    values = [v for v in scores.values() if isinstance(v, (int, float))]
    if values:
        state["total_score"] = sum(values) / len(values)
    else:
        state["total_score"] = 0.0
    state["current_status"] = "scored"
    return state


def outreach_node(state: AgentState) -> AgentState:
    """Outreach agent: initiate contact via best available channel."""
    if state["current_status"] != "scored":
        state["error"] = "Cannot outreach: record not scored"
        return state

    channels = state.get("contact_channels") or []
    if "email" in channels:
        state["last_contact_type"] = "email"
    elif "phone" in channels or "voice" in channels:
        state["last_contact_type"] = "voice"
    elif "sms" in channels:
        state["last_contact_type"] = "sms"
    else:
        state["error"] = "No contact method available"
        return state

    state["interactions_count"] = state.get("interactions_count", 0) + 1
    state["current_status"] = "contacted"
    return state


def engagement_node(state: AgentState) -> AgentState:
    """CRM agent: handle engagement and follow-ups."""
    if state["current_status"] != "contacted":
        state["error"] = "Invalid transition to engaged"
        return state
    state["current_status"] = "engaged"
    state["next_action"] = "schedule_meeting"
    return state


def meeting_node(state: AgentState) -> AgentState:
    """Calendar agent: book meetings."""
    if state["current_status"] != "engaged":
        state["error"] = "Cannot book meeting: not engaged"
        return state
    state["current_status"] = "meeting_booked"
    state["next_action"] = "send_proposal"
    return state


def proposal_node(state: AgentState) -> AgentState:
    """Sales agent: send proposal."""
    if state["current_status"] != "meeting_booked":
        state["error"] = "Cannot send proposal: meeting not booked"
        return state
    state["current_status"] = "proposal_sent"
    state["next_action"] = "follow_up"
    return state


def close_won_node(state: AgentState) -> AgentState:
    """Close won: transition to customer success."""
    state["current_status"] = "closed_won"
    state["next_action"] = "onboarding"
    return state


def close_lost_node(state: AgentState) -> AgentState:
    """Close lost: schedule reactivation."""
    state["current_status"] = "closed_lost"
    state["next_action"] = "reactivate_in_90_days"
    return state


# ============ CONDITIONAL EDGES ============

def should_outreach(state: AgentState) -> str:
    """Decide if record is worth outreach based on total_score."""
    score = state.get("total_score") or 0
    if score >= 50:
        return "outreach"
    return "nurture"


def after_contact(state: AgentState) -> str:
    """Determine next step after contact."""
    if state.get("error"):
        return "error"
    return "wait_for_response"


# ============ BUILD GRAPH ============

def build_object_graph() -> StateGraph:
    """Build and return a generic object lifecycle state graph.
    
    This graph is metadata-aware: the nodes operate on generic AgentState
    which carries `object_name` + `data`. Callers resolve field semantics
    via the metadata engine before/after graph execution.
    """
    workflow = StateGraph(AgentState)

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
            "nurture": END,
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


# Global compiled graph instance (metadata-aware, generic)
object_graph = build_object_graph()


# Legacy compatibility alias
lead_graph = object_graph
