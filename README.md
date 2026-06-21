# LocaScanScribe.AI

**Local-first document search with OCR, Markdown recognition, and a Google-like UI.**

**Локальный поисковик по документам с OCR, распознаванием в Markdown и интерфейсом в стиле Google.**

![Local-first](https://img.shields.io/badge/local--first-yes-16a34a)
![Docker](https://img.shields.io/badge/docker-compose-2563eb)
![Vue 3](https://img.shields.io/badge/Vue-3-42b883)
![FastAPI](https://img.shields.io/badge/FastAPI-Python%203.12-009688)
![llama.cpp](https://img.shields.io/badge/llama.cpp-GPU-7c3aed)

---

## English

### What Is It?

LocaScanScribe.AI is a local document search application for PDFs, images, Office files, and text/Markdown documents. It converts uploaded files into readable Markdown, keeps the original file available for download, and exposes a clean search experience with document links and matching snippets.

The project is designed for private, local workflows: OCR and embeddings run through local `llama.cpp` Docker services, and the app is orchestrated with Docker Compose.

### Highlights

- **Local OCR pipeline**: PDF pages are rendered into images, then recognized by a local OCR model through an OpenAI-compatible `llama.cpp` API.
- **GPU-ready model serving**: OCR and embedding services run with CUDA-enabled `llama.cpp` containers.
- **Markdown-first documents**: recognized content is shown as rich Markdown with math/formula rendering support.
- **Google-like search UI**: search box, answer card, document links, and matching snippets.
- **Upload workflows**: PDF, images, Office files, text, and Markdown upload tabs.
- **Document management**: list, open, rename, delete, download original, and download recognized Markdown.
- **Internationalized UI**: English and Russian interface.
- **Docker Compose stack**: frontend, backend, PostgreSQL, Qdrant, Redis, MinIO, OCR model, and embedding model services.

### Current Status

The application is functional as a local prototype with real OCR, upload, document listing, Markdown preview, and search endpoints.

Important: document metadata and recognized content are currently stored in the backend in-memory repository. After a backend restart or container rebuild, uploaded documents disappear. PostgreSQL, MinIO, and Qdrant are already part of the stack and are the intended persistence layer for the next implementation step.

### Architecture

```text
apps/
  backend/      FastAPI API, ingestion, parsing, OCR orchestration
  frontend/     Vue 3 + Pinia + PrimeVue client
deploy/
  docker-compose.yml
model/
  local GGUF model files, ignored by git
```

Runtime services:

- `frontend`: Vue 3 application served on `http://localhost:3000`
- `backend`: FastAPI API served on `http://localhost:8000`
- `llama-ocr`: local OCR model server
- `llama-embedding`: local embedding model server
- `postgres`: metadata persistence target
- `qdrant`: vector search persistence target
- `redis`: background processing/cache target
- `minio`: original document storage target

### Models

Model binaries are intentionally local-only and ignored by Git. Put them in `model/`:

- `GLM-OCR-Q8_0.gguf`
- `mmproj-GLM-OCR-Q8_0.gguf`
- `Qwen3-Embedding-0.6B-Q8_0.gguf`

The embedding service runs with:

```text
--embedding --pooling last
```

### Quick Start

Requirements:

- Docker Desktop
- NVIDIA GPU + NVIDIA Container Toolkit for GPU inference
- Local GGUF files in `model/`

Run:

```bash
cp .env.example .env
docker compose -f deploy/docker-compose.yml up -d --build
```

Open:

- Frontend: `http://localhost:3000`
- Backend OpenAPI: `http://localhost:8000/docs`
- MinIO Console: `http://localhost:9001`
- Qdrant: `http://localhost:6333`

### OCR Flow

```text
PDF upload
  -> render each page to an image
  -> send each page image to llama.cpp OCR
  -> collect page Markdown
  -> show recognized Markdown in the browser
```

Images go directly to OCR. Office and text formats go through the parser path.

### Roadmap

- Persist metadata and recognized Markdown in PostgreSQL.
- Store original files in MinIO.
- Generate embeddings for Markdown chunks.
- Store vectors in Qdrant.
- Add durable background jobs.
- Add tests and CI.
- Improve OCR post-processing for tables and formulas.

---

## Русский

### Что Это?

LocaScanScribe.AI — локальное приложение для поиска по PDF, изображениям, Office-файлам, текстовым и Markdown-документам. Загруженные файлы распознаются и приводятся к читаемому Markdown, оригинал остаётся доступен для скачивания, а поиск показывает документы и фрагменты совпадений.

Проект ориентирован на приватный локальный сценарий: OCR и embeddings работают через локальные Docker-сервисы `llama.cpp`, всё поднимается через Docker Compose.

### Возможности

- **Локальный OCR pipeline**: страницы PDF сначала превращаются в изображения, затем отправляются в OCR-модель через OpenAI-compatible API `llama.cpp`.
- **GPU inference**: OCR и embedding модели запускаются в CUDA-контейнерах `llama.cpp`.
- **Markdown-first подход**: распознанный документ отображается как визуальный Markdown с поддержкой формул.
- **Поиск в стиле Google**: строка поиска, карточка ответа, ссылки на документы и фрагменты совпадений.
- **Загрузка документов**: вкладки для PDF, изображений, Office-файлов, текста и Markdown.
- **CRUD документов**: список, открытие, переименование, удаление, скачивание оригинала и распознанного Markdown.
- **i18n**: интерфейс на русском и английском.
- **Docker Compose стек**: frontend, backend, PostgreSQL, Qdrant, Redis, MinIO, OCR и embedding модели.

### Текущий Статус

Приложение уже работает как локальный прототип: есть OCR, загрузка, список документов, Markdown preview и поисковые API.

Важно: сейчас metadata, оригиналы и распознанный Markdown хранятся в in-memory репозитории backend. После перезапуска backend или пересборки контейнера загруженные документы исчезают. PostgreSQL, MinIO и Qdrant уже подключены в Docker Compose и запланированы как постоянный слой хранения на следующем этапе.

### Архитектура

```text
apps/
  backend/      FastAPI API, ingestion, parsing, OCR orchestration
  frontend/     Vue 3 + Pinia + PrimeVue client
deploy/
  docker-compose.yml
model/
  локальные GGUF модели, не попадают в Git
```

Сервисы:

- `frontend`: Vue 3 приложение на `http://localhost:3000`
- `backend`: FastAPI API на `http://localhost:8000`
- `llama-ocr`: локальный OCR model server
- `llama-embedding`: локальный embedding model server
- `postgres`: целевое хранение metadata
- `qdrant`: целевое хранение векторов
- `redis`: очередь/кэш для фоновой обработки
- `minio`: целевое хранение оригинальных файлов

### Модели

Файлы моделей локальные и игнорируются Git. Положите их в `model/`:

- `GLM-OCR-Q8_0.gguf`
- `mmproj-GLM-OCR-Q8_0.gguf`
- `Qwen3-Embedding-0.6B-Q8_0.gguf`

Embedding service запускается с:

```text
--embedding --pooling last
```

### Быстрый Старт

Требования:

- Docker Desktop
- NVIDIA GPU + NVIDIA Container Toolkit для GPU inference
- GGUF модели в `model/`

Запуск:

```bash
cp .env.example .env
docker compose -f deploy/docker-compose.yml up -d --build
```

Открыть:

- Frontend: `http://localhost:3000`
- Backend OpenAPI: `http://localhost:8000/docs`
- MinIO Console: `http://localhost:9001`
- Qdrant: `http://localhost:6333`

### OCR Flow

```text
Загрузка PDF
  -> каждая страница рендерится в изображение
  -> изображение каждой страницы отправляется в llama.cpp OCR
  -> результаты собираются в Markdown по страницам
  -> распознанный Markdown отображается в браузере
```

Изображения сразу идут в OCR. Office и текстовые форматы идут через parser path.

### Roadmap

- Сохранять metadata и распознанный Markdown в PostgreSQL.
- Хранить оригинальные файлы в MinIO.
- Генерировать embeddings для Markdown chunks.
- Хранить vectors в Qdrant.
- Добавить устойчивые background jobs.
- Добавить tests и CI.
- Улучшить OCR post-processing для таблиц и формул.

