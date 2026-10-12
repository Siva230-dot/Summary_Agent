def truncate_text(
    text: str,
    max_characters: int = 12000,
) -> str:
    """
    Limit text size before sending it to the LLM.

    This is a character-based safety limit.
    """

    if len(text) <= max_characters:
        return text

    return (
        text[:max_characters]
        + "\n\n[Content truncated]"
    )