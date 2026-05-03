"""
Metadata-aware Research Agent.

Enriches ANY object registered in the metadata engine by:
1. Reading the object's field definitions
2. Using LLM to analyze available data and infer missing fields
3. Running web research when URL/website fields are present
4. Generating scores and insights based on field configuration
"""

import json
import logging
from typing import Any, Dict, List, Optional

from app.agents.metadata_context import MetadataContext
from app.agents.research.finder import WebsiteFinder
from app.agents.research.analyzers.website import WebsiteAnalyzer
from app.utils.ai_client import generate_completion
from app.models.object_metadata import ObjectMetadata
from app.models.field_metadata import FieldType

logger = logging.getLogger(__name__)


class MetadataAwareResearchAgent:
    """Research agent that works with any metadata-defined object."""

    def __init__(self, db=None):
        self.website_finder = WebsiteFinder()
        self.website_analyzer = WebsiteAnalyzer()
        self.db = db

    async def enrich(
        self,
        object_meta: ObjectMetadata,
        record_data: Dict[str, Any],
        workspace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Enrich a dynamic record based on its metadata definition.

        Args:
            object_meta: The ObjectMetadata definition
            record_data: Current data dict from the DynamicRecord
            workspace_id: Optional workspace scope

        Returns:
            Enriched data dict (merge this into existing record data)
        """
        logger.info(f"MetadataAwareResearchAgent: enriching {object_meta.name_singular} '{record_data.get('label', '')}'")

        enriched: Dict[str, Any] = {}
        field_map = {f.name: f for f in object_meta.fields}

        # 1. Find website if object has a URL/website field and it's empty
        website_field = next(
            (f for f in object_meta.fields if f.type == FieldType.URL and "web" in f.name.lower()),
            None,
        )
        website_url = record_data.get(website_field.name) if website_field else None
        if website_field and not website_url:
            # Try to find website from label/name + city
            label = record_data.get("label", "")
            city = record_data.get("city", "")
            state = record_data.get("state", "")
            try:
                found = await self.website_finder.find_website(label, city, state)
                if found:
                    enriched[website_field.name] = found
                    website_url = found
                    logger.info(f"Found website for {label}: {found}")
            except Exception as e:
                logger.warning(f"Website finder failed for {label}: {e}")

        # 2. Analyze website if available
        website_analysis: Dict[str, Any] = {}
        if website_url:
            try:
                website_analysis = await self.website_analyzer.analyze(website_url)
                # Map analysis results to fields if they exist
                for field in object_meta.fields:
                    if field.name in enriched or field.name in record_data:
                        continue
                    if field.type == FieldType.TEXT and "tech" in field.name.lower():
                        enriched[field.name] = ", ".join(website_analysis.get("technologies_detected", []))
                    elif field.type == FieldType.TEXT and "service" in field.name.lower():
                        enriched[field.name] = ", ".join(website_analysis.get("services", []))
                    elif field.type == FieldType.TEXT and "about" in field.name.lower():
                        enriched[field.name] = website_analysis.get("about_text", "")[:500]
                    elif field.type == FieldType.BOOLEAN and "chatbot" in field.name.lower():
                        enriched[field.name] = website_analysis.get("has_chatbot", False)
                    elif field.type == FieldType.BOOLEAN and "booking" in field.name.lower():
                        enriched[field.name] = website_analysis.get("has_booking", False)
                    elif field.type == FieldType.BOOLEAN and "ecommerce" in field.name.lower():
                        enriched[field.name] = website_analysis.get("has_ecommerce", False)
            except Exception as e:
                logger.warning(f"Website analysis failed for {website_url}: {e}")

        # 3. AI-powered enrichment for remaining empty fields
        ai_fields = [
            f for f in object_meta.fields
            if not f.is_system
            and not f.is_read_only
            and f.name not in record_data
            and f.name not in enriched
            and f.type in (FieldType.TEXT, FieldType.NUMBER, FieldType.SELECT, FieldType.BOOLEAN)
        ]

        if ai_fields:
            try:
                ai_result = await self._run_ai_enrichment(object_meta, record_data, website_analysis, ai_fields)
                for field in ai_fields:
                    if field.name in ai_result:
                        enriched[field.name] = ai_result[field.name]
            except Exception as e:
                logger.error(f"AI enrichment failed: {e}")

        # 4. Score calculation if score fields exist
        score_fields = [f for f in object_meta.fields if "score" in f.name.lower() and f.type in (FieldType.NUMBER, FieldType.CURRENCY)]
        if score_fields:
            try:
                scores = await self._run_ai_scoring(object_meta, {**record_data, **enriched, **website_analysis}, score_fields)
                for field in score_fields:
                    if field.name in scores:
                        enriched[field.name] = max(0, min(100, float(scores[field.name])))
            except Exception as e:
                logger.error(f"AI scoring failed: {e}")

        # Cleanup
        try:
            await self.website_finder.close()
        except Exception:
            pass
        try:
            await self.website_analyzer.close()
        except Exception:
            pass

        return enriched

    async def _run_ai_enrichment(
        self,
        object_meta: ObjectMetadata,
        record_data: Dict[str, Any],
        website_analysis: Dict[str, Any],
        target_fields: List[Any],
    ) -> Dict[str, Any]:
        """Use LLM to fill missing fields based on available data."""

        field_descriptions = "\n".join(
            f"- {f.name} ({f.type}): {f.description or 'No description'}"
            for f in target_fields
        )

        system_prompt = f"""You are an expert data enrichment assistant.

You are enriching a record of type "{object_meta.label_singular}".
Analyze the available data and infer values for the missing fields.

Return ONLY a valid JSON object with these exact keys and appropriate values:
{chr(10).join(f'- "{f.name}": <value>' for f in target_fields)}

Field types guide:
- TEXT: string
- NUMBER: number
- BOOLEAN: true/false
- SELECT: one of the allowed values
- EMAIL: valid email string
- URL: valid URL string
- PHONE: phone number string

Rules:
1. Only include fields you can reasonably infer from the data.
2. If you cannot infer a field, omit it from the JSON.
3. Be concise. Numbers should be realistic.
4. Return ONLY the JSON object, no markdown, no explanation.
"""

        context = f"""Object Type: {object_meta.label_singular}
Current Data:
{json.dumps(record_data, indent=2, default=str)}

Website Analysis:
{json.dumps(website_analysis, indent=2, default=str)}

Fields to fill:
{field_descriptions}
"""

        response = await generate_completion(
            system_prompt=system_prompt,
            user_prompt=context,
            temperature=0.3,
            max_tokens=2000,
            json_mode=True,
        )

        try:
            return json.loads(response)
        except (json.JSONDecodeError, ValueError):
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except (json.JSONDecodeError, ValueError):
                    pass
            logger.error("AI enrichment returned invalid JSON")
            return {}

    async def _run_ai_scoring(
        self,
        object_meta: ObjectMetadata,
        record_data: Dict[str, Any],
        score_fields: List[Any],
    ) -> Dict[str, Any]:
        """Use LLM to calculate scores for an object."""

        score_descriptions = "\n".join(
            f"- {f.name}: {f.description or 'Score 0-100'}"
            for f in score_fields
        )

        system_prompt = f"""You are an expert scoring analyst for business records.

Score this {object_meta.label_singular} based on the available data.
Return ONLY a valid JSON object with numeric score fields.

Score rules:
- Each score must be a number between 0 and 100.
- Be objective and consistent.
- Return ONLY the JSON object.
"""

        context = f"""Object Type: {object_meta.label_singular}
Data:
{json.dumps(record_data, indent=2, default=str)}

Score fields to calculate:
{score_descriptions}
"""

        response = await generate_completion(
            system_prompt=system_prompt,
            user_prompt=context,
            temperature=0.2,
            max_tokens=1000,
            json_mode=True,
        )

        try:
            result = json.loads(response)
            # Clamp all scores
            for f in score_fields:
                if f.name in result:
                    result[f.name] = max(0, min(100, float(result[f.name])))
            return result
        except (json.JSONDecodeError, ValueError, TypeError):
            logger.error("AI scoring returned invalid JSON")
            return {}
