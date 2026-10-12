from pydantic import BaseModel


class SummarizeResponse(BaseModel):
    source: str
    title: str
    what_it_is: str

    original_word_count: int
    summary_word_count: int
    compression_percentage: float

    summary: str

    quality: str
    retry_count: int