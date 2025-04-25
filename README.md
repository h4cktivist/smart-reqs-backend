## SmartReqs - сервис для автоматического определения требований проекта по его описанию

![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white)

**Цель проекта:** Создать веб-приложение, которое позволит пользователям отправлять описание своих проектов и автоматически получать список технологий (фреймворки, библиотеки и СУБД), применимых для реализации.

### Установка и локальный запуск

Клонировать репозиторий и установить зависимости:
```sh
git clone https://github.com/h4cktivist/smart-reqs-backend.git
cd smart-reqs-backend
pip install - r requirements.txt
```

Создать `.env` файл со следующими переменными окружения:
```txt
MONGO_URI=[URI базы данных MongoDB]
MONGO_DB=[Название базы данных]

SECRET_KEY=[Секретный ключ]
ALGORITHM=[Алгоритм хеширования паролей]
ACCESS_TOKEN_EXPIRE_MINUTES=[Время жизни токена авторизации (мин.)]

LLM_PROVIDER_URL=[URL провайдера LLM через библиотеку OpenAI]
LLM_API_KEY=[API ключ для доступа к LLM]
LLM_NAME=[Название LLM]
```

Запустить:
```sh
uvicorn main:app
```

**Документация**: `/docs`

**Фронтенд**: *https://github.com/h4cktivist/smart-reqs-frontend*
