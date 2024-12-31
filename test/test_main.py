import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from fastapi_pagination import add_pagination

add_pagination(app)


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/post/recent", params={"page": 1, "size": 10})
    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "page": 1,
        "size": 10,
        "total": 0,
        "pages": 0,
    }
