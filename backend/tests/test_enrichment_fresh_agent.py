"""Batch enrichment must use a fresh ResearchAgent per lead.

ResearchAgent.enrich() closes its HTTP clients in `finally`, so an agent is
single-use. Reusing one across a batch made every lead after the first fail
its website fetch ("Cannot send a request, as the client has been closed")
and get scored by the LLM with no website data — and no email found.
Seen in production on 2026-10-02 with the 45-dentist pilot.
"""

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from app.models.lead import LeadStatus
from app.schemas.lead import LeadEnrichment


class SingleUseAgent:
    """Behaves like ResearchAgent: after one enrich() its clients are closed."""

    used_after_close = []

    def __init__(self):
        self.closed = False

    async def enrich(self, lead):
        SingleUseAgent.used_after_close.append(self.closed)
        self.closed = True
        return LeadEnrichment(urgency_score=70, fit_score=80)


class FakeResult:
    def __init__(self, rows):
        self.rows = rows

    def scalars(self):
        return self

    def all(self):
        return self.rows

    def scalar_one_or_none(self):
        return self.rows[0] if self.rows else None


class FakeSession:
    """Returns the queued results in order, one per execute()."""

    def __init__(self, results):
        self.results = list(results)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def execute(self, statement):
        return self.results.pop(0)

    async def commit(self):
        pass


def make_leads(n):
    return [
        SimpleNamespace(id=i, business_name=f"Clinic {i}", status=LeadStatus.DISCOVERED,
                        urgency_score=None, fit_score=None, total_score=None)
        for i in range(1, n + 1)
    ]


@pytest.fixture(autouse=True)
def reset_agent_log():
    SingleUseAgent.used_after_close = []


@pytest.mark.asyncio
async def test_scheduled_enrichment_never_reuses_a_closed_agent():
    from app.tasks.scheduled import _enrich_pending_leads_async

    leads = make_leads(3)
    session = FakeSession([FakeResult(leads)])
    with patch("app.tasks.scheduled.AsyncSessionLocal", return_value=session), \
         patch("app.tasks.scheduled.ResearchAgent", SingleUseAgent):
        result = await _enrich_pending_leads_async()

    assert SingleUseAgent.used_after_close == [False, False, False]
    assert result == {"enriched": 3, "skipped": 0}
    assert all(lead.status == LeadStatus.SCORED for lead in leads)


@pytest.mark.asyncio
async def test_dashboard_batch_enrichment_never_reuses_a_closed_agent():
    from app.api.v1 import leads as leads_api

    leads = make_leads(3)
    session = FakeSession([FakeResult([lead]) for lead in leads])

    async def no_embedding(lead):
        return None

    with patch("app.db.base.AsyncSessionLocal", return_value=session), \
         patch.object(leads_api, "ResearchAgent", SingleUseAgent), \
         patch.object(leads_api, "update_lead_embedding", no_embedding):
        await leads_api._enrich_leads_batch([lead.id for lead in leads])

    assert SingleUseAgent.used_after_close == [False, False, False]
    assert all(lead.status == LeadStatus.SCORED for lead in leads)
