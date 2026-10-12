from urllib.parse import urlparse

from langchain_community.document_loaders import WebBaseLoader


MAX_TEXT_CHARACTERS = 30000


def validate_text(text: str) -> str:
    """
    Validate and normalize input text.
    """

    if not isinstance(text, str):
        raise ValueError(
            "Text must be a string."
        )

    text = text.strip()

    if not text:
        raise ValueError(
            "Text cannot be empty."
        )

    if len(text) < 20:
        raise ValueError(
            "Text is too short to summarize. "
            "Please provide at least 20 characters."
        )

    if len(text) > MAX_TEXT_CHARACTERS:
        raise ValueError(
            f"Text is too long. Maximum allowed "
            f"length is {MAX_TEXT_CHARACTERS} characters."
        )

    return text


def validate_url(url: str) -> str:
    """
    Validate URL.
    """

    url = url.strip()

    parsed = urlparse(url)

    if parsed.scheme not in (
        "http",
        "https",
    ):
        raise ValueError(
            "URL must start with http:// or https://"
        )

    if not parsed.netloc:
        raise ValueError(
            "Invalid URL."
        )

    return url


def fetch_url_content(url: str):
    """
    Fetch readable content from a webpage.
    """

    loader = WebBaseLoader(
        web_paths=[url]
    )

    documents = loader.load()

    if not documents:
        raise ValueError(
            "Could not extract content from the URL."
        )

    text_parts = []

    for document in documents:

        if document.page_content:
            text_parts.append(
                document.page_content
            )

    text = "\n\n".join(
        text_parts
    ).strip()

    if not text:
        raise ValueError(
            "The webpage does not contain readable content."
        )

    # Limit webpage content before sending to the LLM
    if len(text) > MAX_TEXT_CHARACTERS:
        text = text[:MAX_TEXT_CHARACTERS]

    title = ""

    if documents:
        title = documents[0].metadata.get(
            "title",
            ""
        )

    return text, title