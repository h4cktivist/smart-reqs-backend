import pytest
from httpx import AsyncClient, ASGITransport

from main import app, lifespan

PREFIX = '/api/libraries'

EXPERT_USER = {
    'email': 'ivan@example.com',
    'password': 'strongpassword123'
}

NON_EXPERT_USER = {
    'email': 'ivan1@example.com',
    'password': 'strongpassword123'
}

TEST_LIBRARY = {
    "name": "string",
    "language": "string",
    "purpose": "string",
    "licence_type": "string",
}

UPD_TEST_LIBRARY = {
    "name": "updated",
    "language": "string",
    "purpose": "string",
    "licence_type": "string",
}


@pytest.mark.asyncio
async def test_read_libraries():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            res = await ac.get(PREFIX + '/')
            assert res.status_code == 200

            library_id = res.json()[0]['id']
            one_fr_res = await ac.get(PREFIX + f'/{library_id}')
            assert one_fr_res.status_code == 200
            assert list(one_fr_res.json().keys()) == ['name', 'language', 'purpose', 'licence_type', 'id']


@pytest.mark.asyncio
async def test_read_invalid_id_library():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            res = await ac.get(PREFIX + '/invalid_id')
            assert res.status_code == 400


@pytest.mark.asyncio
async def test_read_fake_id_library():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            res = await ac.get(PREFIX + '/681748e522e8e92a00080fbb')
            assert res.status_code == 404


@pytest.mark.asyncio
async def test_crud_non_expert():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            auth_res = await ac.post('/api/auth/login', json=NON_EXPERT_USER)
            token = auth_res.json()['access_token']

            add_res = await ac.post(PREFIX + '/', headers={'Authorization': f'Bearer {token}'}, json=TEST_LIBRARY)
            assert add_res.status_code == 403
            upd_res = await ac.put(PREFIX + '/67e58b9803a98312f2ff8de2',
                                   headers={'Authorization': f'Bearer {token}'}, json=TEST_LIBRARY)
            assert upd_res.status_code == 403
            del_res = await ac.delete(PREFIX + '/67e58b9803a98312f2ff8de2',
                                      headers={'Authorization': f'Bearer {token}'})
            assert del_res.status_code == 403


@pytest.mark.asyncio
async def test_crud_expert():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            auth_res = await ac.post('/api/auth/login', json=EXPERT_USER)
            token = auth_res.json()['access_token']

            add_res = await ac.post(PREFIX + '/', headers={'Authorization': f'Bearer {token}'}, json=TEST_LIBRARY)
            library_id = add_res.json()['id']
            assert add_res.status_code == 200
            assert list(add_res.json().keys()) == ['name', 'language', 'purpose', 'licence_type', 'id']
            upd_res = await ac.put(PREFIX + f"/{library_id}",
                                   headers={'Authorization': f'Bearer {token}'}, json=UPD_TEST_LIBRARY)
            assert upd_res.status_code == 200
            assert upd_res.json()['name'] == 'updated'
            del_res = await ac.delete(PREFIX + f"/{library_id}",
                                      headers={'Authorization': f'Bearer {token}'})
            assert del_res.status_code == 200
            find_res = await ac.get(PREFIX + f"/{library_id}")
            assert find_res.status_code == 404
