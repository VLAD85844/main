# Tasks SPA + FastAPI

Простое приложение для управления задачами (SPA + REST API). Реализованы добавление, отображение, изменение статуса, удаление; фильтрация по статусу; анимации; базовая адаптивность. Тесты на бэкенде. Докеризация фронта и бэка.

## Стек
- Frontend: React 18, Vite, TypeScript, CSS
- Backend: FastAPI, SQLAlchemy, Pydantic v2, SQLite, Uvicorn
- Tests: pytest
- Docker: Dockerfile (оба сервиса), docker-compose

## Структура проекта
```
backend/
  app/
    __init__.py
    main.py           # FastAPI приложение (+ CORS, health)
    db.py             # Подключение к SQLite, SessionLocal, Base
    models.py         # SQLAlchemy модель Task
    schemas.py        # Pydantic-схемы (v2) для запросов/ответов
    crud.py           # CRUD-операции над Task
    routers/
      tasks.py        # Эндпоинты /api/tasks
  tests/
    test_tasks.py     # 3 теста: create, list, update
  requirements.txt
  Dockerfile

frontend/
  index.html
  package.json
  tsconfig.json
  vite.config.ts
  Dockerfile
  src/
    main.tsx
    App.tsx
    api.ts
    types.ts
    styles.css

docker-compose.yml
README.md
```

## Бэкенд (локальный запуск)
Требуется Python 3.11+
```powershell
cd backend
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Проверка:
- Health: http://localhost:8000/health
- Swagger: http://localhost:8000/docs

## Тесты (бэкенд)
```powershell
cd backend
. .\.venv\Scripts\Activate.ps1
pytest -q
```
Ожидание: 3 passed.

## Фронтенд (локальный запуск)
Требуется Node 20+
```powershell
cd frontend
npm install
npm run dev
```
Открыть: http://localhost:5173 (запросы проксируются на http://localhost:8000/api)

## Запуск через Docker
```powershell
docker compose up --build
```
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## REST API (основное)
Базовый URL: `http://localhost:8000/api/tasks`

- GET `/` — список задач
  - query: `status` (optional) one of `pending|in_progress|done`
- POST `/` — создать задачу
  - body: `{ title: string, description?: string }`
- GET `/{id}` — получить одну
- PATCH `/{id}` — обновить
  - body: `{ title?, description?, status? }`
- DELETE `/{id}` — удалить

Модель задачи:
```json
{
  "id": 1,
  "title": "string",
  "description": "string|null",
  "status": "pending|in_progress|done",
  "created_at": "ISO8601"
}
```

## Фронтенд функциональность
- Список задач с полями `title`, `description`, `status`.
- Добавление новой задачи через форму.
- Переключение статуса по кругу: pending → in_progress → done → pending.
- Удаление задачи.
- Фильтрация по статусу (кнопки).
- Простая анимация появления карточек.
- Базовая адаптивность (320–1440px).

## Замечания реализации
- БД: SQLite, файл создаётся автоматически. Датавремя хранится в UTC (`DateTime(timezone=True)`).
- Pydantic v2: схемы настроены через `ConfigDict(from_attributes=True)`.
- CORS открыт для dev (в `app.main`).

## Что можно расширить
- Alembic миграции.
- Редактирование title/description на фронтенде.
- Пагинация и сортировка списка.
- Логи/конфиги (ENV) и CI (линт/тест).
- Тесты фронтенда (RTL).

## Быстрые команды
- Backend dev: `uvicorn app.main:app --reload`
- Frontend dev: `npm run dev`
- Tests: `pytest -q`
- Docker (оба): `docker compose up --build`


