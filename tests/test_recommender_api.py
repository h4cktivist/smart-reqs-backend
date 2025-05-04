import pytest
from httpx import AsyncClient, ASGITransport

from main import app, lifespan


PREFIX = '/api/recommender'

USER = {
    'email': 'ivan@example.com',
    'password': 'strongpassword123'
}

TEST_VALID_POJECT_SHORT = {
    "title": "FinanceHelper",
    "idea_description": "Приложение помогает пользователям контролировать доходы и расходы, ставить финансовые цели и "
                        "анализировать свои траты. Оно предоставляет простой и интуитивно понятный интерфейс для "
                        "учета денежных потоков с возможностью категоризации расходов и визуализации статистики.",
    "functional_reqs": "- Добавление и редактирование доходов/расходов с привязкой к категориям. - Настройка "
                       "финансовых целей (например, накопление суммы) и отслеживание прогресса. - Генерация отчетов и "
                       "графиков по тратам за выбранный период. - Синхронизация данных между несколькими "
                       "устройствами. - Возможность экспорта данных в CSV или PDF.",
}

TEST_INVALID_POJECT_SHORT = {
    "title": "string",
    "idea_description": "string",
    "functional_reqs": "string"
}

TEST_VALID_POJECT_LONG = {
    "title": "string",
    "idea_description": "string",
    "functional_reqs": "string",
    "product_type": "веб-приложение",
    "db_needed": True,
    "big_data_needed": False,
    "data_structure": "SQL",
    "data_analysis_needed": False,
    "ml_needed": False,
    "languages_preferences": ["Python"],
    "licensing_type": "открытая",
    "scaling_needed": True,
    "autotesting_needed": True
}


@pytest.mark.asyncio
async def test_unauthorized_history():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            res = await ac.get(PREFIX + '/history')
            assert res.status_code == 401


@pytest.mark.asyncio
async def test_history():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            auth_res = await ac.post('/api/auth/login', json=USER)
            token = auth_res.json()['access_token']

            res = await ac.get(PREFIX + '/history', headers={'Authorization': f'Bearer {token}'})
            assert res.status_code == 200


@pytest.mark.asyncio
async def test_recommender_valid_short_req():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            auth_res = await ac.post('/api/auth/login', json=USER)
            token = auth_res.json()['access_token']

            res = await ac.post(PREFIX + '/', headers={'Authorization': f'Bearer {token}'},
                                json=TEST_VALID_POJECT_SHORT)
            assert res.status_code == 200
            assert list(res.json().keys()) == ['_id', 'request_id', 'frameworks', 'libraries',
                                               'databases', 'min_devs', 'max_devs']


@pytest.mark.asyncio
async def test_recommender_invalid_short_req():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            auth_res = await ac.post('/api/auth/login', json=USER)
            token = auth_res.json()['access_token']

            res = await ac.post(PREFIX + '/', headers={'Authorization': f'Bearer {token}'},
                                json=TEST_INVALID_POJECT_SHORT)
            assert res.status_code == 400


@pytest.mark.asyncio
async def test_recommender_valid_long_req():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            auth_res = await ac.post('/api/auth/login', json=USER)
            token = auth_res.json()['access_token']

            res = await ac.post(PREFIX + '/', headers={'Authorization': f'Bearer {token}'},
                                json=TEST_VALID_POJECT_LONG)
            assert res.status_code == 200
            assert list(res.json().keys()) == ['_id', 'request_id', 'frameworks', 'libraries',
                                               'databases', 'min_devs', 'max_devs']


@pytest.mark.asyncio
async def test_history_delete():
    async with lifespan(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url='http://test'
        ) as ac:
            auth_res = await ac.post('/api/auth/login', json=USER)
            token = auth_res.json()['access_token']

            res = await ac.get(PREFIX + '/history', headers={'Authorization': f'Bearer {token}'})
            req_id = res.json()[0]
            del_res = await ac.delete(PREFIX + f'/history/{req_id}', headers={'Authorization': f'Bearer {token}'})
            assert del_res.status_code == 200
