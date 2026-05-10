import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

_INVALID_PATTERNS = [
    r"^.*@example\.(com|org|net)$",
    r"^.*@test\.(com|org|net)$",
    r"^.*@localhost$",
    r"^.*@domain\.com$",
    r"^.*@email\.com$",
    r"^.*@\.com$",
    r"^.*@\.co$",
    r"^.*@gmail\.co$",
]

_INVALID_REGEX = [re.compile(p, re.IGNORECASE) for p in _INVALID_PATTERNS]


def sanitize_email(raw: Optional[str], source: str = "unknown") -> Optional[str]:
    if not raw or not isinstance(raw, str):
        return None
    cleaned = raw.strip().lower()
    if not cleaned:
        return None
    if not _EMAIL_REGEX.match(cleaned):
        logger.debug(f"[email:sanitize] Invalid email from {source}: {raw}")
        return None
    for pattern in _INVALID_REGEX:
        if pattern.match(cleaned):
            logger.debug(f"[email:sanitize] Invalid pattern from {source}: {raw}")
            return None
    return cleaned
