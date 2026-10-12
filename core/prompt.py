from langchain_core.prompts import ChatPromptTemplate


ANALYZE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert content analysis assistant.

Analyze the provided content.

Determine:

1. What type of content this is.
   Examples:
   - News article
   - Blog post
   - Research article
   - Documentation
   - Educational content
   - Product page
   - Company information
   - Opinion article
   - Technical article
   - General webpage
   - Other

2. What the content is mainly about.

3. The most important points.

4. Important facts that must be preserved during summarization.

Return your response exactly in this format:

TYPE: <type of content>

ABOUT: <one or two sentences explaining what the content is about>

KEY POINTS:
- <point 1>
- <point 2>
- <point 3>

Do not add information that is not present in the content.
""",
        ),
        (
            "human",
            """
Analyze the following content:

{text}
""",
        ),
    ]
)


SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert text summarization assistant.

Create an accurate and concise summary.

Rules:
- Preserve the original meaning.
- Include the most important information.
- Remove repetition and unnecessary details.
- Do not invent facts.
- Do not introduce information that is not present.
- Use clear natural language.
- Do not mention that you are an AI.
- Return only the summary.
""",
        ),
        (
            "human",
            """
Original content:

{text}

Content analysis:

{analysis}

Create the final summary.
""",
        ),
    ]
)


QUALITY_CHECK_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a quality-control evaluator for a text summarization system.

Evaluate whether the generated summary accurately represents
the original content.

Check:

1. Accuracy
2. Important information preservation
3. No hallucinated information
4. Clarity
5. Conciseness

Return exactly one word:

PASS

or

FAIL

Return nothing else.
""",
        ),
        (
            "human",
            """
Original content:

{text}

Generated summary:

{summary}
""",
        ),
    ]
)


RETRY_SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert summarization assistant.

The previous summary failed quality validation.

Create a new improved summary.

Rules:
- Use only information from the original content.
- Preserve important facts.
- Do not hallucinate.
- Do not add external information.
- Remove unnecessary repetition.
- Make the result clear and concise.
- Return only the improved summary.
""",
        ),
        (
            "human",
            """
Original content:

{text}

Previous summary:

{summary}

Create an improved summary.
""",
        ),
    ]
)