from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        description="Text that needs to be summarized.",
        min_length=20,
        max_length=50000,
    )


class URLSummarizeRequest(BaseModel):
    url: str = Field(
        ...,
        description="URL of the webpage to summarize.",
    )