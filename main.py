from contextlib import asynccontextmanager

import confident_trace as ct

from fastapi import FastAPI

from api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("======================================")
    print("Starting Confident AI tracing...")
    print("======================================")

    ct.init()

    print("Confident AI tracing initialized.")

    yield

    print("Shutting down Confident AI tracing...")

    ct.shutdown()

    print("Confident AI tracing shutdown complete.")


app = FastAPI(
    title="Text Summarizer Agent",
    description=(
        "AI Text Summarization Agent using "
        "LangGraph, LangChain and Groq."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Text Summarizer Agent is running",
        "status": "healthy",
    }