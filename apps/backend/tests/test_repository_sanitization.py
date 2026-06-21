from app.ingestion.repository import _clean_postgres_text


def test_clean_postgres_text_removes_nul_bytes() -> None:
    assert _clean_postgres_text("A\x00B") == "AB"
