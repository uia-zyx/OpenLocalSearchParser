# LocaScanScribe.AI

Local document search with OCR, Markdown extraction, and vector search.

## Stack

- Frontend: Vue 3, TypeScript, Pinia, PrimeVue, Vite.
- Backend: Python 3.12, FastAPI.
- Storage: PostgreSQL, Qdrant, Redis, MinIO.
- Models: local `llama.cpp` servers for OCR and embeddings.

## Local Models

Model binaries are local-only and ignored by git. Put these files in `model/`:

- `GLM-OCR-Q8_0.gguf`
- `Qwen3-Embedding-0.6B-Q8_0.gguf`

The embedding server must run with `--embedding --pooling last`.

## Quick Start

```bash
cp .env.example .env
docker compose -f deploy/docker-compose.yml up --build
```

Open:

- Frontend: `http://localhost:3000`
- Backend OpenAPI: `http://localhost:8000/docs`
- MinIO Console: `http://localhost:9001`
- Qdrant: `http://localhost:6333`

## Current Implementation

This is the first implementation slice:

- Monorepo structure.
- Docker Compose stack.
- FastAPI upload/search endpoints.
- Vue Google-like search UI.
- Upload tabs for PDF/PBF, images, Office, and text/Markdown.
- Local-only model folder ignored by git.

The current parser/search path is intentionally minimal and will be replaced by real PostgreSQL, MinIO, Qdrant, OCR, parser, and embedding implementations in the next slices.

