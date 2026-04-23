import httpx
from typing import Optional, Dict
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class WebsiteAnalyzer:
    """Analyze a business website to extract insights."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=15.0,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )
    
    async def analyze(self, url: str) -> Dict:
        """
        Fetch and analyze a website.
        
        Returns:
            Dict with: title, description, technologies_detected, has_chatbot,
            has_booking, has_contact_form, social_links, email_found
        """
        if not url.startswith("http"):
            url = f"https://{url}"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return {"error": str(e), "url": url}
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract basic info
        title = soup.title.string.strip() if soup.title else ""
        
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc else ""
        
        if not description:
            og_desc = soup.find("meta", attrs={"property": "og:description"})
            description = og_desc["content"] if og_desc else ""
        
        # Detect technologies
        html_text = response.text.lower()
        technologies = []
        
        tech_indicators = {
            "WordPress": "wp-content",
            "Shopify": "myshopify",
            "Squarespace": "squarespace",
            "Wix": "wix",
            "React": "react",
            "Vue": "vue",
            "Angular": "angular",
            "Stripe": "stripe",
            "PayPal": "paypal",
            "Calendly": "calendly",
            "HubSpot": "hubspot",
            "Mailchimp": "mailchimp",
            "Google Analytics": "google-analytics",
            "Facebook Pixel": "fbevents",
            "Intercom": "intercom",
            "Zendesk": "zendesk",
            "Drift": "drift",
        }
        
        for tech, indicator in tech_indicators.items():
            if indicator in html_text:
                technologies.append(tech)
        
        # Detect features
        has_chatbot = any(
            indicator in html_text
            for indicator in ["chatbot", "livechat", "intercom", "drift", "tawk", "crisp"]
        )
        
        has_booking = any(
            indicator in html_text
            for indicator in ["book", "schedule", "appointment", "reservation", "calendly"]
        )
        
        has_contact_form = bool(soup.find("form")) or "contact" in html_text
        
        # Extract social links
        social_links = {}
        social_domains = {
            "facebook": "facebook.com",
            "instagram": "instagram.com",
            "twitter": "twitter.com",
            "linkedin": "linkedin.com",
            "youtube": "youtube.com",
            "tiktok": "tiktok.com",
        }
        
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            for platform, domain in social_domains.items():
                if domain in href and platform not in social_links:
                    social_links[platform] = a["href"]
        
        # Try to find email on page
        email_found = None
        import re
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        emails = email_pattern.findall(response.text)
        if emails:
            # Filter out common false positives
            filtered = [e for e in emails if not any(x in e.lower() for x in ["example", "test@", "noreply"])]
            if filtered:
                email_found = filtered[0]
        
        return {
            "url": url,
            "title": title,
            "description": description,
            "technologies_detected": technologies,
            "has_chatbot": has_chatbot,
            "has_booking": has_booking,
            "has_contact_form": has_contact_form,
            "social_links": social_links,
            "email_found": email_found,
        }
    
    async def close(self):
        await self.client.aclose()
