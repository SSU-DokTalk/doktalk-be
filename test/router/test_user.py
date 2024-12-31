import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from fastapi_pagination import add_pagination
import json

add_pagination(app)


@pytest.mark.anyio
async def test_basicRegisterController():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post(
            "/user/register",
            data=json.dumps(
                {
                    "email": "user@example.com",
                    "password": "testtest123@",
                    "name": "test",
                    "profile": "",
                }
            ),
        )
        assert response.status_code == 409
