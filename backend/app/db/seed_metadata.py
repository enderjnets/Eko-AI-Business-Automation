"""Seed script: registers all existing Eko AI models as ObjectMetadata + FieldMetadata.

This is idempotent — safe to run multiple times. It only creates records that don't
already exist (matched by name_singular + workspace_id=NULL).
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.object_metadata import ObjectMetadata
from app.models.field_metadata import FieldMetadata, FieldType

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Standard object definitions
# ---------------------------------------------------------------------------

STANDARD_OBJECTS = [
    {
        "name_singular": "lead",
        "name_plural": "leads",
        "label_singular": "Lead",
        "label_plural": "Leads",
        "description": "A prospective customer or business",
        "icon": "IconUser",
        "target_table_name": "leads",
        "is_system": True,
        "position": 1,
    },
    {
        "name_singular": "deal",
        "name_plural": "deals",
        "label_singular": "Deal",
        "label_plural": "Deals",
        "description": "A sales opportunity tied to a lead",
        "icon": "IconCurrencyDollar",
        "target_table_name": "deals",
        "is_system": True,
        "position": 2,
    },
    {
        "name_singular": "campaign",
        "name_plural": "campaigns",
        "label_singular": "Campaign",
        "label_plural": "Campaigns",
        "description": "A marketing or outreach campaign",
        "icon": "IconTarget",
        "target_table_name": "campaigns",
        "is_system": True,
        "position": 3,
    },
    {
        "name_singular": "email_sequence",
        "name_plural": "email_sequences",
        "label_singular": "Email Sequence",
        "label_plural": "Email Sequences",
        "description": "Automated email sequence with steps",
        "icon": "IconMail",
        "target_table_name": "email_sequences",
        "is_system": True,
        "position": 4,
    },
    {
        "name_singular": "booking",
        "name_plural": "bookings",
        "label_singular": "Booking",
        "label_plural": "Bookings",
        "description": "A scheduled meeting or demo",
        "icon": "IconCalendar",
        "target_table_name": "bookings",
        "is_system": True,
        "position": 5,
    },
    {
        "name_singular": "phone_call",
        "name_plural": "phone_calls",
        "label_singular": "Phone Call",
        "label_plural": "Phone Calls",
        "description": "A voice call with a lead",
        "icon": "IconPhone",
        "target_table_name": "phone_calls",
        "is_system": True,
        "position": 6,
    },
    {
        "name_singular": "proposal",
        "name_plural": "proposals",
        "label_singular": "Proposal",
        "label_plural": "Proposals",
        "description": "A sales proposal sent to a lead",
        "icon": "IconFileDescription",
        "target_table_name": "proposals",
        "is_system": True,
        "position": 7,
    },
    {
        "name_singular": "payment",
        "name_plural": "payments",
        "label_singular": "Payment",
        "label_plural": "Payments",
        "description": "A payment transaction",
        "icon": "IconCreditCard",
        "target_table_name": "payments",
        "is_system": True,
        "position": 8,
    },
    {
        "name_singular": "user",
        "name_plural": "users",
        "label_singular": "User",
        "label_plural": "Users",
        "description": "A system user",
        "icon": "IconUsers",
        "target_table_name": "users",
        "is_system": True,
        "position": 9,
    },
    {
        "name_singular": "interaction",
        "name_plural": "interactions",
        "label_singular": "Interaction",
        "label_plural": "Interactions",
        "description": "An engagement with a lead (email, call, note)",
        "icon": "IconMessage",
        "target_table_name": "interactions",
        "is_system": True,
        "position": 10,
    },
]


# ---------------------------------------------------------------------------
# Field definitions per object (subset of most important fields)
# ---------------------------------------------------------------------------

LEAD_FIELDS = [
    {"name": "business_name", "label": "Business Name", "type": FieldType.TEXT, "is_nullable": False, "is_label_field": True, "position": 1},
    {"name": "category", "label": "Category", "type": FieldType.TEXT, "position": 2},
    {"name": "email", "label": "Email", "type": FieldType.EMAIL, "position": 3},
    {"name": "phone", "label": "Phone", "type": FieldType.PHONE, "position": 4},
    {"name": "website", "label": "Website", "type": FieldType.URL, "position": 5},
    {"name": "address", "label": "Address", "type": FieldType.TEXT, "position": 6},
    {"name": "city", "label": "City", "type": FieldType.TEXT, "position": 7},
    {"name": "state", "label": "State", "type": FieldType.TEXT, "position": 8},
    {"name": "zip_code", "label": "Zip Code", "type": FieldType.TEXT, "position": 9},
    {"name": "status", "label": "Status", "type": FieldType.SELECT, "options": [
        {"value": "discovered", "label": "Discovered", "color": "gray"},
        {"value": "enriched", "label": "Enriched", "color": "blue"},
        {"value": "scored", "label": "Scored", "color": "yellow"},
        {"value": "contacted", "label": "Contacted", "color": "orange"},
        {"value": "engaged", "label": "Engaged", "color": "teal"},
        {"value": "meeting_booked", "label": "Meeting Booked", "color": "purple"},
        {"value": "proposal_sent", "label": "Proposal Sent", "color": "indigo"},
        {"value": "negotiating", "label": "Negotiating", "color": "pink"},
        {"value": "closed_won", "label": "Closed Won", "color": "green"},
        {"value": "closed_lost", "label": "Closed Lost", "color": "red"},
    ], "position": 10},
    {"name": "source", "label": "Source", "type": FieldType.SELECT, "options": [
        {"value": "google_maps", "label": "Google Maps"},
        {"value": "linkedin", "label": "LinkedIn"},
        {"value": "yelp", "label": "Yelp"},
        {"value": "colorado_sos", "label": "Colorado SOS"},
        {"value": "manual", "label": "Manual"},
        {"value": "referral", "label": "Referral"},
    ], "position": 11},
    {"name": "urgency_score", "label": "Urgency Score", "type": FieldType.NUMBER, "settings": {"decimals": 0, "min": 0, "max": 100}, "position": 12},
    {"name": "fit_score", "label": "Fit Score", "type": FieldType.NUMBER, "settings": {"decimals": 0, "min": 0, "max": 100}, "position": 13},
    {"name": "total_score", "label": "Total Score", "type": FieldType.NUMBER, "settings": {"decimals": 0, "min": 0, "max": 100}, "position": 14},
    {"name": "do_not_contact", "label": "Do Not Contact", "type": FieldType.BOOLEAN, "position": 15},
    {"name": "owner_id", "label": "Owner", "type": FieldType.RELATION, "relation_target_object_id": None, "position": 16},
    {"name": "assigned_to", "label": "Assigned To", "type": FieldType.TEXT, "position": 17},
    {"name": "tags", "label": "Tags", "type": FieldType.MULTI_SELECT, "position": 18},
    {"name": "notes", "label": "Notes", "type": FieldType.RICH_TEXT, "position": 19},
    {"name": "next_follow_up_at", "label": "Next Follow Up", "type": FieldType.DATE_TIME, "position": 20},
    {"name": "embedding", "label": "Embedding", "type": FieldType.VECTOR, "is_read_only": True, "position": 21},
]

DEAL_FIELDS = [
    {"name": "lead_id", "label": "Lead", "type": FieldType.RELATION, "is_nullable": False, "position": 1},
    {"name": "name", "label": "Deal Name", "type": FieldType.TEXT, "is_nullable": False, "is_label_field": True, "position": 2},
    {"name": "value", "label": "Value", "type": FieldType.CURRENCY, "settings": {"currency": "USD", "decimals": 2}, "position": 3},
    {"name": "probability", "label": "Probability (%)", "type": FieldType.NUMBER, "settings": {"decimals": 0, "min": 0, "max": 100}, "position": 4},
    {"name": "status", "label": "Status", "type": FieldType.SELECT, "options": [
        {"value": "prospecting", "label": "Prospecting"},
        {"value": "qualification", "label": "Qualification"},
        {"value": "proposal", "label": "Proposal"},
        {"value": "negotiation", "label": "Negotiation"},
        {"value": "closed_won", "label": "Closed Won", "color": "green"},
        {"value": "closed_lost", "label": "Closed Lost", "color": "red"},
    ], "position": 5},
    {"name": "expected_close_date", "label": "Expected Close", "type": FieldType.DATE, "position": 6},
    {"name": "actual_close_date", "label": "Actual Close", "type": FieldType.DATE, "position": 7},
    {"name": "assigned_to", "label": "Assigned To", "type": FieldType.TEXT, "position": 8},
]

CAMPAIGN_FIELDS = [
    {"name": "name", "label": "Name", "type": FieldType.TEXT, "is_nullable": False, "is_label_field": True, "position": 1},
    {"name": "description", "label": "Description", "type": FieldType.RICH_TEXT, "position": 2},
    {"name": "campaign_type", "label": "Type", "type": FieldType.SELECT, "options": [
        {"value": "discovery", "label": "Discovery"},
        {"value": "outreach", "label": "Outreach"},
        {"value": "follow_up", "label": "Follow Up"},
        {"value": "reactivation", "label": "Reactivation"},
        {"value": "referral", "label": "Referral"},
    ], "position": 3},
    {"name": "status", "label": "Status", "type": FieldType.SELECT, "options": [
        {"value": "draft", "label": "Draft"},
        {"value": "active", "label": "Active", "color": "green"},
        {"value": "paused", "label": "Paused", "color": "yellow"},
        {"value": "completed", "label": "Completed", "color": "blue"},
        {"value": "archived", "label": "Archived", "color": "gray"},
    ], "position": 4},
]

BOOKING_FIELDS = [
    {"name": "title", "label": "Title", "type": FieldType.TEXT, "is_nullable": False, "is_label_field": True, "position": 1},
    {"name": "lead_id", "label": "Lead", "type": FieldType.RELATION, "position": 2},
    {"name": "attendee_email", "label": "Attendee Email", "type": FieldType.EMAIL, "position": 3},
    {"name": "attendee_name", "label": "Attendee Name", "type": FieldType.TEXT, "position": 4},
    {"name": "start_time", "label": "Start Time", "type": FieldType.DATE_TIME, "position": 5},
    {"name": "end_time", "label": "End Time", "type": FieldType.DATE_TIME, "position": 6},
    {"name": "status", "label": "Status", "type": FieldType.SELECT, "options": [
        {"value": "pending", "label": "Pending"},
        {"value": "confirmed", "label": "Confirmed"},
        {"value": "cancelled", "label": "Cancelled"},
        {"value": "completed", "label": "Completed"},
        {"value": "no_show", "label": "No Show"},
    ], "position": 7},
]

USER_FIELDS = [
    {"name": "email", "label": "Email", "type": FieldType.EMAIL, "is_nullable": False, "is_unique": True, "is_label_field": True, "position": 1},
    {"name": "full_name", "label": "Full Name", "type": FieldType.TEXT, "position": 2},
    {"name": "role", "label": "Role", "type": FieldType.SELECT, "options": [
        {"value": "admin", "label": "Admin"},
        {"value": "manager", "label": "Manager"},
        {"value": "agent", "label": "Agent"},
    ], "position": 3},
    {"name": "is_active", "label": "Active", "type": FieldType.BOOLEAN, "position": 4},
]

# Map object name -> field list
OBJECT_FIELDS_MAP = {
    "lead": LEAD_FIELDS,
    "deal": DEAL_FIELDS,
    "campaign": CAMPAIGN_FIELDS,
    "booking": BOOKING_FIELDS,
    "user": USER_FIELDS,
}


# ---------------------------------------------------------------------------
# Seed runner
# ---------------------------------------------------------------------------

async def seed_metadata(db: AsyncSession) -> None:
    """Idempotent seed of standard objects and fields into metadata tables."""
    for obj_def in STANDARD_OBJECTS:
        # Check if already exists
        stmt = select(ObjectMetadata).where(
            ObjectMetadata.name_singular == obj_def["name_singular"],
            ObjectMetadata.workspace_id.is_(None),
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            logger.info(f"Object '{obj_def['name_singular']}' already seeded — skipping")
            continue

        # Create object metadata
        obj = ObjectMetadata(
            workspace_id=None,
            **obj_def,
        )
        db.add(obj)
        await db.flush()
        logger.info(f"Created object metadata: {obj_def['name_singular']} (id={obj.id})")

        # Create fields
        field_defs = OBJECT_FIELDS_MAP.get(obj_def["name_singular"], [])
        for fdef in field_defs:
            field = FieldMetadata(
                workspace_id=None,
                object_metadata_id=obj.id,
                is_system=True,
                **fdef,
            )
            db.add(field)

        await db.flush()
        logger.info(f"Created {len(field_defs)} fields for {obj_def['name_singular']}")

    await db.commit()
    logger.info("Metadata seed completed successfully")
