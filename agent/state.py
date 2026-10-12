from typing import TypedDict


class SummarizerState(TypedDict):
    text: str
    source_url: str
    title: str

    analysis: str
    what_it_is: str

    summary: str

    original_word_count: int
    summary_word_count: int
    compression_percentage: float

    quality: str
    retry_count: int