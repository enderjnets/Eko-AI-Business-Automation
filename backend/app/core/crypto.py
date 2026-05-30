"""Symmetric encryption for secrets stored at rest (control plane service/agent keys).

Uses Fernet (AES-128-CBC + HMAC) with a key derived deterministically from
``settings.SECRET_KEY`` so no extra secret needs to be provisioned. The same
SECRET_KEY that signs JWTs therefore also protects instance credentials — keep
it stable and out of source control.
"""
import base64
import hashlib
import logging

from cryptography.fernet import Fernet, InvalidToken

from app.config import get_settings

logger = logging.getLogger(__name__)

_fernet: Fernet | None = None


def _get_fernet() -> Fernet:
    """Lazily build a Fernet instance keyed off SECRET_KEY."""
    global _fernet
    if _fernet is None:
        settings = get_settings()
        secret = (settings.SECRET_KEY or "eko-dev-secret").encode("utf-8")
        # Fernet requires a url-safe base64-encoded 32-byte key.
        digest = hashlib.sha256(secret).digest()
        _fernet = Fernet(base64.urlsafe_b64encode(digest))
    return _fernet


def encrypt(plaintext: str | None) -> str | None:
    """Encrypt a string for storage. Returns None for empty input."""
    if not plaintext:
        return None
    token = _get_fernet().encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt(ciphertext: str | None) -> str | None:
    """Decrypt a stored string. Returns None on empty or undecryptable input."""
    if not ciphertext:
        return None
    try:
        return _get_fernet().decrypt(ciphertext.encode("utf-8")).decode("utf-8")
    except (InvalidToken, ValueError) as e:
        logger.error(f"Failed to decrypt control plane secret: {e}")
        return None
