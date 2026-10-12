from core.llm import llm

from core.prompt import (
    ANALYZE_PROMPT,
    SUMMARY_PROMPT,
    QUALITY_CHECK_PROMPT,
    RETRY_SUMMARY_PROMPT,
)

from core.text_utils import truncate_text

from agent.state import SummarizerState


def count_words(text: str) -> int:
    """
    Count the number of words in a text.
    """

    if not text:
        return 0

    return len(text.split())


def calculate_compression(
    original_count: int,
    summary_count: int,
) -> float:
    """
    Calculate the percentage of text reduction.

    Example:
        Original = 100 words
        Summary = 20 words

        Compression = 80%
    """

    if original_count == 0:
        return 0.0

    compression = (
        1 - (summary_count / original_count)
    ) * 100

    return round(compression, 2)


def analyze_node(
    state: SummarizerState,
) -> SummarizerState:
    """
    Analyze the content before summarization.

    Determines:
    - Content type
    - What the content is about
    - Important points
    """

    # Keep the LLM request within a safe size.
    text = truncate_text(
        state["text"],
        max_characters=10000,
    )

    prompt = ANALYZE_PROMPT.invoke(
        {
            "text": text,
        }
    )

    response = llm.invoke(prompt)

    analysis = response.content.strip()

    # Default value in case the LLM doesn't
    # return the expected TYPE format.
    what_it_is = "General content"

    for line in analysis.splitlines():

        if line.upper().startswith("TYPE:"):

            what_it_is = line.split(
                ":",
                1,
            )[1].strip()

            break

    return {
        **state,
        "analysis": analysis,
        "what_it_is": what_it_is,
    }


def summarize_node(
    state: SummarizerState,
) -> SummarizerState:
    """
    Generate the initial summary.
    """

    # Limit content sent to the LLM.
    text = truncate_text(
        state["text"],
        max_characters=10000,
    )

    analysis = state["analysis"]

    prompt = SUMMARY_PROMPT.invoke(
        {
            "text": text,
            "analysis": analysis,
        }
    )

    response = llm.invoke(prompt)

    summary = response.content.strip()

    # Word counts are calculated from the
    # original full content and final summary.
    original_word_count = count_words(
        state["text"]
    )

    summary_word_count = count_words(
        summary
    )

    compression_percentage = calculate_compression(
        original_word_count,
        summary_word_count,
    )

    return {
        **state,
        "summary": summary,
        "original_word_count": original_word_count,
        "summary_word_count": summary_word_count,
        "compression_percentage": compression_percentage,
    }


def quality_check_node(
    state: SummarizerState,
) -> SummarizerState:
    """
    Check whether the generated summary
    accurately represents the source content.
    """

    # Use a smaller amount of source content
    # for the quality-check request to reduce
    # Groq token usage.
    text = truncate_text(
        state["text"],
        max_characters=8000,
    )

    summary = state["summary"]

    prompt = QUALITY_CHECK_PROMPT.invoke(
        {
            "text": text,
            "summary": summary,
        }
    )

    response = llm.invoke(prompt)

    quality = response.content.strip().upper()

    if "PASS" in quality:
        quality = "PASS"
    else:
        quality = "FAIL"

    return {
        **state,
        "quality": quality,
    }


def retry_summary_node(
    state: SummarizerState,
) -> SummarizerState:
    """
    Generate an improved summary if the
    quality check fails.
    """

    text = truncate_text(
        state["text"],
        max_characters=10000,
    )

    summary = state["summary"]

    prompt = RETRY_SUMMARY_PROMPT.invoke(
        {
            "text": text,
            "summary": summary,
        }
    )

    response = llm.invoke(prompt)

    improved_summary = response.content.strip()

    # Recalculate metrics after retry.
    summary_word_count = count_words(
        improved_summary
    )

    compression_percentage = calculate_compression(
        state["original_word_count"],
        summary_word_count,
    )

    return {
        **state,
        "summary": improved_summary,
        "summary_word_count": summary_word_count,
        "compression_percentage": compression_percentage,
        "retry_count": state["retry_count"] + 1,
    }