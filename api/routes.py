from fastapi import APIRouter, HTTPException
import confident_trace as ct
from schemas.request import (
    SummarizeRequest,
    URLSummarizeRequest,
)

from schemas.response import SummarizeResponse

from core.validation import (
    validate_text,
    validate_url,
    fetch_url_content,
)

from agent.graph import summarizer_graph


router = APIRouter(
    prefix="/api",
    tags=["Text Summarizer"],
)


def run_summarizer(
    text: str,
    source: str,
    title: str = "",
):
    """
    Run the LangGraph summarizer with
    Confident AI tracing.
    """

    initial_state = {
        "text": text,
        "source_url": source,
        "title": title,

        "analysis": "",
        "what_it_is": "",

        "summary": "",

        "original_word_count": 0,
        "summary_word_count": 0,
        "compression_percentage": 0.0,

        "quality": "",
        "retry_count": 0,
    }

    with ct.span(
        "text-summarizer-agent",
        type="agent",
    ):

        result = summarizer_graph.invoke(
            initial_state
        )

        ct.update_trace(
            input=text,
            output=result["summary"],
            metadata={
                "source": source,
                "content_type": result["what_it_is"],
                "agent": "text-summarizer",
                "agent_version": "1.0.0",
            },
        )

        return result


@router.post(
    "/summarize",
    response_model=SummarizeResponse,
)
def summarize_text(
    request: SummarizeRequest,
):
    """
    Summarize directly provided text.
    """

    try:

        text = validate_text(
            request.text
        )

        result = run_summarizer(
            text=text,
            source="text",
        )

        return SummarizeResponse(
            source="text",
            title="",
            what_it_is=result["what_it_is"],
            original_word_count=result[
                "original_word_count"
            ],
            summary_word_count=result[
                "summary_word_count"
            ],
            compression_percentage=result[
                "compression_percentage"
            ],
            summary=result["summary"],
            quality=result["quality"],
            retry_count=result["retry_count"],
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:

        print(
            f"Text summarization error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to summarize the text.",
        )


@router.post(
    "/summarize-url",
    response_model=SummarizeResponse,
)
def summarize_url(
    request: URLSummarizeRequest,
):
    """
    Fetch a webpage and summarize its content.
    """

    try:

        url = validate_url(
            request.url
        )

        text, title = fetch_url_content(
            url
        )

        result = run_summarizer(
            text=text,
            source=url,
            title=title,
        )

        return SummarizeResponse(
            source=url,
            title=title,
            what_it_is=result["what_it_is"],
            original_word_count=result[
                "original_word_count"
            ],
            summary_word_count=result[
                "summary_word_count"
            ],
            compression_percentage=result[
                "compression_percentage"
            ],
            summary=result["summary"],
            quality=result["quality"],
            retry_count=result["retry_count"],
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:

        print(
            f"URL summarization error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to fetch or summarize "
                "the webpage."
            ),
        )