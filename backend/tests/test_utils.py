import pytest
from datetime import timedelta
from time import sleep

from src.utils import create_jwt_token, create_access_token, create_refresh_token, verify_token
from src.dependencies import get_current_user

from src.exceptions import AuthenticationError


@pytest.mark.asyncio
async def test_create_jwt_token():
    data = {"sub": "testname"}
    expires_delta = timedelta(minutes=30)

    jwt_token = create_jwt_token(data, expires_delta)
    assert jwt_token is not None


@pytest.mark.asyncio
async def test_create_access_token():
    data = {"sub": "testname"}
    access_token = create_access_token(data)
    assert access_token is not None


@pytest.mark.asyncio
async def test_create_refresh_token():
    data = {"sub": "testname"}
    access_token = create_refresh_token(data)
    assert access_token is not None


@pytest.mark.asyncio
async def test_verify_token():
    data = {"sub": "testname"}
    access_token = create_access_token(data)
    assert access_token is not None

    payload = verify_token(access_token)
    assert payload["sub"] == "testname"


@pytest.mark.asyncio
async def test_verify_token_invalid():
    with pytest.raises(AuthenticationError):
        jwt_token = "invalid_token"
        verify_token(jwt_token)


@pytest.mark.asyncio
async def test_verify_token_expiry():
    with pytest.raises(AuthenticationError):
        data = {"sub": "testname"}
        expires_delta = timedelta(milliseconds=499)
        jwt_token = create_jwt_token(data, expires_delta)
        assert jwt_token is not None

        sleep(0.5)
        verify_token(jwt_token)
