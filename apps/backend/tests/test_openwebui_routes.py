from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.api.openwebui_utils import document_id_from_url, validate_openwebui_key
from app.core.settings import Settings


def test_document_id_from_frontend_url() -> None:
    document_id = uuid4()

    parsed_id = document_id_from_url(f"http://localhost:3000/documents/{document_id}?tab=preview")

    assert parsed_id == document_id


def test_openwebui_auth_accepts_bearer_key() -> None:
    settings = Settings(openwebui_web_search_api_key="secret")

    validate_openwebui_key(settings, "Bearer secret", None)


def test_openwebui_auth_rejects_wrong_key() -> None:
    settings = Settings(openwebui_web_search_api_key="secret")

    with pytest.raises(HTTPException):
        validate_openwebui_key(settings, "Bearer wrong", None)
