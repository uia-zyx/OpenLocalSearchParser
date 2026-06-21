from app.parsers.registry import ParserRegistry


def test_markdown_post_processing_removes_wrapping_fence_and_extra_spaces() -> None:
    registry = ParserRegistry()

    markdown = registry._post_process_ocr_markdown(
        "```markdown\n"
        "# Title   \n\n\n"
        "Formula: $ x + y $\n"
        "```"
    )

    assert markdown == "# Title\n\nFormula: $x + y$"


def test_markdown_post_processing_removes_nul_bytes() -> None:
    registry = ParserRegistry()

    markdown = registry._post_process_ocr_markdown("A\x00B\x07\n\nC")

    assert markdown == "AB\n\nC"
