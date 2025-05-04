import pytest
from httpx import AsyncClient, ASGITransport

from main import app, lifespan


PREFIX = '/api/auth'


@pytest.mark.asyncio
async def test_read_user_me_unauthorized():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as ac:
        res = await ac.get(PREFIX + '/me')
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_user_valid_registration():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            user_data = {
                'username': 'string',
                'email': 'user@example.com',
                'password': 'string'
            }
            res = await ac.post(PREFIX + '/register', json=user_data)
            assert res.status_code == 200
            assert '_id' in dict(res.json()).keys()


@pytest.mark.asyncio
async def test_user_invalid_registration():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as ac:
        user_data = {
            'username': 'string',
            'email': 'user@example.com',
        }
        res = await ac.post(PREFIX + '/register', json=user_data)
        assert res.status_code == 422


@pytest.mark.asyncio
async def test_user_login():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            user_data = {
                'email': 'user@example.com',
                'password': 'string'
            }
            res = await ac.post(PREFIX + '/login', json=user_data)
            assert res.status_code == 200
            assert ['access_token', 'token_type', 'expires_in'] == list(res.json().keys())

            token = res.json()['access_token']
            me_res = await ac.get(PREFIX + '/me', headers={'Authorization': f'Bearer {token}'})
            assert me_res.status_code == 200


@pytest.mark.asyncio
async def test_user_profile_update():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            user_data = {
                'email': 'user@example.com',
                'password': 'string'
            }
            res = await ac.post(PREFIX + '/login', json=user_data)
            token = res.json()['access_token']

            upd_user = {
                'username': 'new_username'
            }
            upd_res = await ac.patch(PREFIX + '/me', headers={'Authorization': f'Bearer {token}'}, json=upd_user)
            assert upd_res.status_code == 200
            assert upd_res.json()['username'] == 'new_username'
