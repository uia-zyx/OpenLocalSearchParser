from app.api.schemas import SearchRequest
from app.domain.models import SearchResult, SearchSnippet
from app.ingestion.service import InMemoryDocumentRepository
from app.search.chunking import chunk_markdown


class SearchService:
    def __init__(self, repository: InMemoryDocumentRepository) -> None:
        self.repository = repository

    async def search(self, request: SearchRequest) -> list[SearchResult]:
        query = request.query.casefold()
        results: list[SearchResult] = []

        for document in self.repository.list():
            if request.filters and request.filters.mime_types:
                if document.mime_type not in request.filters.mime_types:
                    continue

            markdown = document.markdown or ""
            chunks = chunk_markdown(document.id, markdown)
            snippets: list[SearchSnippet] = []

            for chunk in chunks:
                if query in chunk.text.casefold():
                    snippets.append(
                        SearchSnippet(
                            chunk_id=chunk.id,
                            phrase=_snippet(chunk.text, request.query),
                            page_number=chunk.page_number,
                            heading_path=chunk.heading_path,
                        )
                    )

            if snippets:
                results.append(
                    SearchResult(
                        document_id=document.id,
                        title=document.title,
                        url=f"/documents/{document.id}",
                        score=1.0,
                        snippets=snippets[:3],
                    )
                )

        return results[: request.limit]


def _snippet(text: str, query: str, radius: int = 120) -> str:
    position = text.casefold().find(query.casefold())
    if position < 0:
        return text[: radius * 2].strip()

    start = max(position - radius, 0)
    end = min(position + len(query) + radius, len(text))
    return text[start:end].strip()

