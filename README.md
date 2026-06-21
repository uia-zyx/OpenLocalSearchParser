# LocaScanScribe.AI

**Local document search and OCR platform with Markdown-based document representation.**

**Локальная платформа для поиска по документам, OCR-обработки и представления распознанного содержимого в Markdown.**

---

## English

### Overview

LocaScanScribe.AI is an application for local deployment that processes PDFs, images, Office files, plain text, and Markdown documents. It stores the original uploaded file, converts recognized content into Markdown, and provides search results with document links and matching text fragments.

The system is designed for environments where document processing should run on local infrastructure. OCR and embedding services are provided by local `llama.cpp` containers, while the application stack is managed with Docker Compose.

### Capabilities

- PDF processing through page rendering and OCR recognition.
- Image OCR through an OpenAI-compatible local model endpoint.
- Parser-based processing for Office, text, and Markdown files.
- Markdown preview for recognized documents and search snippets.
- Document operations: list, open, rename, delete, download original file, and download recognized Markdown.
- Search interface with answer summary, document links, and text fragments.
- Internationalized frontend with English and Russian locales.
- Docker Compose deployment with frontend, backend, PostgreSQL, Qdrant, Redis, MinIO, OCR, and embedding services.

### Current Status

The application currently includes document upload, OCR processing, document listing, Markdown preview, and search endpoints.

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
- `llama-ocr`: OCR model server
- `llama-embedding`: embedding model server
- `postgres`: metadata persistence target
- `qdrant`: vector search persistence target
- `redis`: background processing/cache target
- `minio`: original document storage target

### Models

Model binaries are ignored by Git. Place them in `model/`:

- `GLM-OCR-Q8_0.gguf`
- `mmproj-GLM-OCR-Q8_0.gguf`
- `Qwen3-Embedding-0.6B-Q8_0.gguf`

The embedding service runs with:

```text
--embedding --pooling last
```

### Installation

Requirements:

- Docker Desktop
- NVIDIA GPU and NVIDIA Container Toolkit for GPU inference
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

### PDF OCR Flow

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

### Обзор

LocaScanScribe.AI — приложение для локального развертывания, предназначенное для обработки PDF, изображений, Office-файлов, обычного текста и Markdown-документов. Система сохраняет исходный файл, преобразует распознанное содержимое в Markdown и предоставляет поиск по документам с ссылками и фрагментами совпадений.

Система рассчитана на сценарии, где обработка документов должна выполняться на локальной инфраструктуре. OCR и embeddings обслуживаются локальными контейнерами `llama.cpp`, а весь стек запускается через Docker Compose.

### Возможности

- Обработка PDF через рендеринг страниц и OCR-распознавание.
- OCR изображений через локальный OpenAI-compatible endpoint модели.
- Parser-based обработка Office-файлов, текста и Markdown.
- Markdown preview для распознанных документов и фрагментов поиска.
- Операции с документами: список, открытие, переименование, удаление, скачивание оригинала и распознанного Markdown.
- Поисковый интерфейс с кратким ответом, ссылками на документы и фрагментами совпадений.
- Интерфейс на русском и английском языках.
- Docker Compose стек с frontend, backend, PostgreSQL, Qdrant, Redis, MinIO, OCR и embedding сервисами.

### Текущий Статус

Приложение включает загрузку документов, OCR-обработку, список документов, Markdown preview и поисковые API.

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
- `llama-ocr`: OCR model server
- `llama-embedding`: embedding model server
- `postgres`: целевое хранение metadata
- `qdrant`: целевое хранение векторов
- `redis`: очередь/кэш для фоновой обработки
- `minio`: целевое хранение оригинальных файлов

### Модели

Файлы моделей игнорируются Git. Положите их в `model/`:

- `GLM-OCR-Q8_0.gguf`
- `mmproj-GLM-OCR-Q8_0.gguf`
- `Qwen3-Embedding-0.6B-Q8_0.gguf`

Embedding service запускается с:

```text
--embedding --pooling last
```

### Установка

Требования:

- Docker Desktop
- NVIDIA GPU и NVIDIA Container Toolkit для GPU inference
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

### PDF OCR Flow

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

