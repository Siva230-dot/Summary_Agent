from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from agent.state import SummarizerState

from agent.nodes import (
    analyze_node,
    summarize_node,
    quality_check_node,
    retry_summary_node,
)


def quality_router(state: SummarizerState) -> str:
    """
    Decide whether the summary should be accepted
    or regenerated.
    """

    if state["quality"] == "PASS":
        return "end"

    if state["retry_count"] >= 1:
        return "end"

    return "retry"


def build_graph():
    """
    Build and compile the Text Summarizer LangGraph.
    """

    graph = StateGraph(SummarizerState)

    # Add nodes
    graph.add_node(
        "analyze",
        analyze_node,
    )

    graph.add_node(
        "summarize",
        summarize_node,
    )

    graph.add_node(
        "quality_check",
        quality_check_node,
    )

    graph.add_node(
        "retry_summary",
        retry_summary_node,
    )

    # Starting point
    graph.add_edge(
        START,
        "analyze",
    )

    # Main workflow
    graph.add_edge(
        "analyze",
        "summarize",
    )

    graph.add_edge(
        "summarize",
        "quality_check",
    )

    # Conditional routing
    graph.add_conditional_edges(
        "quality_check",
        quality_router,
        {
            "retry": "retry_summary",
            "end": END,
        },
    )

    # Retry goes directly to the end
    graph.add_edge(
        "retry_summary",
        END,
    )

    return graph.compile()


summarizer_graph = build_graph()