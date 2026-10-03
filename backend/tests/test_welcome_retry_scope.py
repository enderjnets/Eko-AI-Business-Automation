"""The hourly welcome-email retry must only touch landing-page leads.

retry_failed_welcome_emails re-dispatches enrich_and_welcome_lead, which
sends the "AI automation analysis" email. Only the public landing-page form
creates leads that expect it. Without a source filter, any discovered lead
that enrichment found an email for was cold-emailed within the hour: on
2026-10-02 22:11 a Google Maps dentist lead got one, without anyone deciding
to contact it.
"""

from unittest.mock import patch

import importlib
import pkgutil

import pytest
from sqlalchemy.dialects import postgresql

import app.models

# Compiling the statement configures every mapper, and relationships refer to
# models by name (User -> WorkspaceMember, Lead -> Payment...). In production
# the app imports them all; do the same here so the suite's import order
# doesn't matter.
for _module in pkgutil.iter_modules(app.models.__path__):
    importlib.import_module(f"app.models.{_module.name}")


class CapturingSession:
    """Records the statement and returns no rows."""

    def __init__(self):
        self.statements = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def execute(self, statement):
        self.statements.append(statement)

        class NoRows:
            def all(self):
                return []

        return NoRows()


def compiled_sql(statement) -> str:
    return str(statement.compile(dialect=postgresql.dialect(),
                                 compile_kwargs={"literal_binds": True}))


@pytest.mark.asyncio
async def test_retry_selects_only_landing_page_leads():
    from app.tasks.scheduled import _retry_failed_welcome_emails_async

    session = CapturingSession()
    with patch("app.agents.outreach.channels.email._is_quota_breaker_open", return_value=False), \
         patch("app.tasks.scheduled.AsyncSessionLocal", return_value=session):
        result = await _retry_failed_welcome_emails_async()

    assert result == {"retried": 0}
    assert len(session.statements) == 1
    assert "leads.source = 'LANDING_PAGE'" in compiled_sql(session.statements[0])
