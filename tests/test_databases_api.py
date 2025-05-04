import pytest
from httpx import AsyncClient, ASGITransport

from main import app, lifespan

PREFIX = '/api/databases'

EXPERT_USER = {
    'email': 'ivan@example.com',
    'password': 'strongpassword123'
}

NON_EXPERT_USER = {
    'email': 'ivan1@example.com',
    'password': 'strongpassword123'
}

TEST_DATABASE = {
    "name": "string",
    "type": "string",
    "scaling_poss": True,
    "big_data_poss": True,
    "acid_support": True,
    "licence_type": "string"
}

UPD_TEST_DATABASE = {
    "name": "updated",
    "type": "string",
    "scaling_poss": True,
    "big_data_poss": False,
    "acid_support": True,
    "licence_type": "string"
}


@pytest.mark.asyncio
async def test_read_databases():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            res = await ac.get(PREFIX + '/')
            assert res.status_code == 200

            database_id = res.json()[0]['id']
            one_db_res = await ac.get(PREFIX + f'/{database_id}')
            assert one_db_res.status_code == 200
            assert list(one_db_res.json().keys()) == ['name', 'type', 'scaling_poss',
                                                      'big_data_poss', 'acid_support', 'licence_type', 'id']


@pytest.mark.asyncio
async def test_read_invalid_id_database():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            res = await ac.get(PREFIX + '/invalid_id')
            assert res.status_code == 400


@pytest.mark.asyncio
async def test_read_fake_id_database():
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

            add_res = await ac.post(PREFIX + '/', headers={'Authorization': f'Bearer {token}'}, json=TEST_DATABASE)
            assert add_res.status_code == 403
            upd_res = await ac.put(PREFIX + '/67e58b9803a98312f2ff8de2',
                                   headers={'Authorization': f'Bearer {token}'}, json=TEST_DATABASE)
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

            add_res = await ac.post(PREFIX + '/', headers={'Authorization': f'Bearer {token}'}, json=TEST_DATABASE)
            database_id = add_res.json()['id']
            assert add_res.status_code == 200
            assert list(add_res.json().keys()) == ['name', 'type', 'scaling_poss',
                                                   'big_data_poss', 'acid_support', 'licence_type', 'id']
            upd_res = await ac.put(PREFIX + f"/{database_id}",
                                   headers={'Authorization': f'Bearer {token}'}, json=UPD_TEST_DATABASE)
            assert upd_res.status_code == 200
            assert upd_res.json()['name'] == 'updated' and upd_res.json()['big_data_poss'] == False
            del_res = await ac.delete(PREFIX + f"/{database_id}",
                                      headers={'Authorization': f'Bearer {token}'})
            assert del_res.status_code == 200
            find_res = await ac.get(PREFIX + f"/{database_id}")
            assert find_res.status_code == 404
