"""Tests for Research agent."""

import pytest
from unittest.mock import AsyncMock, patch

from app.agents.research.agent import ResearchAgent
from app.schemas.lead import LeadEnrichment


class TestResearchAgent:
    @pytest.mark.asyncio
    async def test_enrich_with_website(self):
        agent = ResearchAgent()
        agent.website_analyzer = AsyncMock()
        agent.website_analyzer.analyze.return_value = {
            "technologies_detected": ["WordPress", "Google Analytics"],
            "social_links": {"facebook": "https://fb.com/test"},
            "title": "Test Business",
            "description": "We do testing",
            "has_chatbot": False,
            "has_booking": True,
            "has_contact_form": True,
        }

        mock_lead = AsyncMock()
        mock_lead.business_name = "Test Business"
        mock_lead.website = "https://test.com"
        mock_lead.category = "Software"
        mock_lead.city = "Denver"
        mock_lead.description = "A test business"
        mock_lead.phone = "555-0000"
        mock_lead.source_data = {}
        mock_lead.id = 1

        with patch(
            "app.agents.research.agent.generate_completion",
            new_callable=AsyncMock,
        ) as mock_completion:
            mock_completion.return_value = '''
            {
                "review_summary": "Solid online presence",
                "trigger_events": ["High growth"],
                "pain_points": ["Missed calls"],
                "urgency_score": 75,
                "fit_score": 80,
                "scoring_reason": "Good fit for AI automation"
            }
            '''

            result = await agent.enrich(mock_lead)

        assert isinstance(result, LeadEnrichment)
        assert result.urgency_score == 75
        assert result.fit_score == 80
        assert result.pain_points == ["Missed calls"]
        assert result.tech_stack == ["WordPress", "Google Analytics"]

    @pytest.mark.asyncio
    async def test_enrich_without_website(self):
        agent = ResearchAgent()
        agent.website_analyzer = AsyncMock()

        mock_lead = AsyncMock()
        mock_lead.business_name = "No Website Biz"
        mock_lead.website = None
        mock_lead.category = "Plumbing"
        mock_lead.city = "Denver"
        mock_lead.description = "Local plumber"
        mock_lead.phone = "555-0000"
        mock_lead.source_data = {}
        mock_lead.id = 2

        with patch(
            "app.agents.research.agent.generate_completion",
            new_callable=AsyncMock,
        ) as mock_completion:
            mock_completion.return_value = '''
            {
                "review_summary": "Limited data",
                "trigger_events": [],
                "pain_points": ["No online booking"],
                "urgency_score": 60,
                "fit_score": 70,
                "scoring_reason": "Moderate fit"
            }
            '''

            result = await agent.enrich(mock_lead)

        assert isinstance(result, LeadEnrichment)
        assert result.urgency_score == 60
        agent.website_analyzer.analyze.assert_not_called()

    def test_run_ai_analysis_fallback(self):
        agent = ResearchAgent()
        mock_lead = AsyncMock()
        mock_lead.business_name = "Bad JSON Biz"
        mock_lead.category = "Retail"
        mock_lead.city = "Denver"
        mock_lead.description = "Shop"
        mock_lead.phone = "555-0000"
        mock_lead.website = None
        mock_lead.source_data = {}

        import asyncio
        result = asyncio.run(agent._run_ai_analysis(mock_lead, {}))
        # Since generate_completion is not patched, it will fail and return fallback
        assert "urgency_score" in result
        assert result["urgency_score"] == 50
