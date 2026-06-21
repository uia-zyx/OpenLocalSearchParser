from dataclasses import dataclass, field
from typing import Protocol

from app.domain.models import ProcessingStrategy


@dataclass(frozen=True)
class StoredFile:
    filename: str
    mime_type: str
    content: bytes


@dataclass(frozen=True)
class ParsedDocument:
    title: str
    markdown: str
    strategy: ProcessingStrategy
    warnings: list[str] = field(default_factory=list)


class DocumentParser(Protocol):
    async def parse(self, file: StoredFile) -> ParsedDocument:
        ...

