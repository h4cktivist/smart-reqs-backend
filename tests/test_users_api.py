import pytest
from httpx import AsyncClient, ASGITransport

from main import app


prefix = "/api/auth"


@pytest.mark.asyncio
async def test_read_user_me_unauthorized():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as ac:
        res = await ac.get(prefix + '/me')
        assert res.status_code == 401
