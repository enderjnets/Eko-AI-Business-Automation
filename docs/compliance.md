# Compliance Controls — Eko AI Business Automation

This document maps each regulatory requirement to its implementation in code.
Maintained as part of the Commit Trio Protocol (AGENTS.md).

---

## Regulation Matrix

| Regulation | Requirement | Implementation | File / Line |
|------------|-------------|----------------|-------------|
| **TCPA** | Consent must be recorded before contact | Lead.consent_status field (pending -> opted_in / opted_out); consent_recorded_at timestamp | app/models/lead.py:122-123 |
| **TCPA** | Do-Not-Contact enforcement | Every outbound channel checks Lead.do_not_contact == False before sending | app/api/v1/crm.py:147, app/api/v1/emails.py:36, app/api/v1/campaigns.py:147, app/api/v1/sequences.py:242, app/api/v1/voice_agent.py:68 |
| **TCPA** | Rate limiting to prevent harassment | MAX_CONTACTS_PER_DAY = 5 per lead; _check_contact_rate_limit() counts outbound interactions in 24h window | app/api/v1/crm.py:37-55 |
| **TCPA** | Cooldown between contact attempts | Celery process_follow_ups skips leads with last_contact_at within 24h | app/tasks/scheduled.py:36-51 |
| **CAN-SPAM** | Functional unsubscribe in every email | unsubscribe_url auto-appended to all outreach emails; handler GET /webhooks/unsubscribe sets do_not_contact=True | app/api/v1/crm.py:404-410, app/api/v1/webhooks.py:246-271 |
| **CAN-SPAM** | Honor opt-out within 10 business days | sync_dnc_registry task runs monthly; auto-marks bounced leads (consent_status=bounced) and archives opt-outs >2 years | app/tasks/scheduled.py:469-518 |
| **CPA Colorado** | Right to deletion | DELETE /api/v1/leads/{id} hard-deletes lead + cascades interactions; audit logged | app/api/v1/leads.py (lead deletion endpoint) |
| **CPA Colorado** | Right to access / portability | GET /api/v1/leads/{id} returns full lead record; GET /api/v1/leads lists all leads with filters | app/api/v1/leads.py |
| **FCC AI Rule** | AI disclosure in outbound communications | Emails include [AI-generated message] disclosure in body; voice assistant Eva self-identifies as AI at call start | app/agents/outreach/channels/email.py:125, app/services/vapi_client.py (Eva assistant config) |
| **FCC AI Rule** | Consent for AI-initiated calls | Voice agent checks do_not_contact and consent_status before placing outbound calls | app/api/v1/voice_agent.py:68 |

---

## Automated Compliance Tasks

| Task | Frequency | Description | File |
|------|-----------|-------------|------|
| sync_dnc_registry | Monthly (cron: 0 2 1 * *) | Marks leads with 3+ bounces as do_not_contact; archives opt-outs older than 2 years | app/tasks/scheduled.py:736-741 |
| process_follow_ups | Every 5 minutes | Sends follow-up emails respecting rate limits, cooldown, and do_not_contact | app/tasks/scheduled.py |
| backup_processed_leads | Every 2 hours | Exports processed leads to JSON backup for audit trail | app/tasks/scheduled.py |

---

## Data Retention

- Active leads: Retained indefinitely (customer relationship).
- Opted-out leads: Archived (soft-delete) after 2 years via sync_dnc_registry.
- Bounced emails: Auto-marked do_not_contact after 3 bounces.
- Backups: Stored in ./backups/ with timestamped JSON files.

---

## Audit Trail

All mutating actions are traced via:
- Paperclip AI: Agent governance, cost tracking, heartbeat logs (PAPERCLIP_API_URL).
- Application logs: Structured JSON logs (level INFO in production).
- Database: Interaction table records every outbound/inbound contact with metadata.

---

*Last updated: 2026-05-10*
