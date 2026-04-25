"""Tests for Authentication system."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_current_admin,
)
from app.models.user import UserRole


class TestPasswordSecurity:
    def test_password_hashing(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_password_hash_different_each_time(self):
        password = "samepassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)


class TestJWTTokens:
    def test_create_access_token(self):
        token = create_access_token(user_id=1)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_access_token(self):
        token = create_access_token(user_id=42)
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "42"
        assert payload["type"] == "access"

    def test_decode_invalid_token(self):
        payload = decode_token("invalid.token.here")
        assert payload is None

    def test_token_expiration(self):
        from jose import jwt as jose_jwt
        from app.config import get_settings
        settings = get_settings()

        token = create_access_token(user_id=1, expires_delta=timedelta(seconds=-1))
        with pytest.raises(Exception):
            jose_jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    def test_create_refresh_token(self):
        token = create_refresh_token(user_id=1)
        payload = decode_token(token)
        assert payload["type"] == "refresh"


class TestGetCurrentUser:
    @pytest.mark.asyncio
    async def test_get_current_user_valid(self):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.is_active = True
        mock_user.role = UserRole.AGENT

        mock_db = AsyncMock()
        mock_db.execute.return_value.scalar_one_or_none.return_value = mock_user

        mock_creds = MagicMock()
        mock_creds.credentials = create_access_token(user_id=1)

        user = await get_current_user(mock_creds, mock_db)
        assert user.id == 1

    @pytest.mark.asyncio
    async def test_get_current_user_no_credentials(self):
        mock_db = AsyncMock()
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(None, mock_db)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self):
        mock_db = AsyncMock()
        mock_creds = MagicMock()
        mock_creds.credentials = "invalid.token"

        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(mock_creds, mock_db)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_get_current_user_inactive(self):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.is_active = False

        mock_db = AsyncMock()
        mock_db.execute.return_value.scalar_one_or_none.return_value = mock_user

        mock_creds = MagicMock()
        mock_creds.credentials = create_access_token(user_id=1)

        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(mock_creds, mock_db)
        assert exc_info.value.status_code == 403


class TestGetCurrentAdmin:
    @pytest.mark.asyncio
    async def test_admin_access_granted(self):
        mock_user = MagicMock()
        mock_user.role = UserRole.ADMIN
        mock_user.is_superuser = False

        result = await get_current_admin(mock_user)
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_manager_access_granted(self):
        mock_user = MagicMock()
        mock_user.role = UserRole.MANAGER
        mock_user.is_superuser = False

        result = await get_current_admin(mock_user)
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_agent_access_denied(self):
        mock_user = MagicMock()
        mock_user.role = UserRole.AGENT
        mock_user.is_superuser = False

        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_admin(mock_user)
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_superuser_access_granted(self):
        mock_user = MagicMock()
        mock_user.role = UserRole.AGENT
        mock_user.is_superuser = True

        result = await get_current_admin(mock_user)
        assert result == mock_user


class TestAuthRouter:
    @pytest.mark.asyncio
    async def test_login_success(self):
        from app.api.v1.auth import login

        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.hashed_password = get_password_hash("password123")
        mock_user.is_active = True

        mock_db = AsyncMock()
        mock_db.execute.return_value.scalar_one_or_none.return_value = mock_user

        req = MagicMock()
        req.email = "test@example.com"
        req.password = "password123"

        result = await login(req, mock_db)
        assert "access_token" in result
        assert "refresh_token" in result
        assert result["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_password(self):
        from app.api.v1.auth import login
        from fastapi import HTTPException

        mock_user = MagicMock()
        mock_user.hashed_password = get_password_hash("correctpassword")
        mock_user.is_active = True

        mock_db = AsyncMock()
        mock_db.execute.return_value.scalar_one_or_none.return_value = mock_user

        req = MagicMock()
        req.email = "test@example.com"
        req.password = "wrongpassword"

        with pytest.raises(HTTPException) as exc_info:
            await login(req, mock_db)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_dev_login_in_production_blocked(self):
        from app.api.v1.auth import dev_login
        from fastapi import HTTPException

        mock_db = AsyncMock()

        with patch("app.api.v1.auth.get_settings") as mock_settings:
            mock_settings.return_value.is_production = True
            with pytest.raises(HTTPException) as exc_info:
                await dev_login(mock_db)
            assert exc_info.value.status_code == 403
