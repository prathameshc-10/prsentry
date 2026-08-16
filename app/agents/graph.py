from langgraph.graph import StateGraph, END, START
from app.agents.state import AgentState
from app.agents.style_agent import style_agent_node
from app.agents.security_agent import security_agent_node
from app.agents.test_coverage_agent import test_coverage_agent_node
from app.agents.synthesis_agent import synthesis_agent_node
from app.github.tools import post_pr_comment


def post_review_node(state: AgentState) -> dict:
    body = f"🤖 **PRSentry Review**\n\n{state['final_review']}"
    post_pr_comment(
        repo_full_name=state["repo_full_name"],
        pr_number=state["pr_number"],
        token=state["installation_token"],
        body=body,
    )
    return {}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("style_agent", style_agent_node)
    graph.add_node("security_agent", security_agent_node)
    graph.add_node("test_coverage_agent", test_coverage_agent_node)
    graph.add_node("synthesis_agent", synthesis_agent_node)
    graph.add_node("post_review", post_review_node)

    # Fan-out: START triggers all three specialist agents in parallel
    graph.add_edge(START, "style_agent")
    graph.add_edge(START, "security_agent")
    graph.add_edge(START, "test_coverage_agent")

    # Fan-in: synthesis waits for all three to complete before running
    graph.add_edge("style_agent", "synthesis_agent")
    graph.add_edge("security_agent", "synthesis_agent")
    graph.add_edge("test_coverage_agent", "synthesis_agent")

    graph.add_edge("synthesis_agent", "post_review")
    graph.add_edge("post_review", END)

    return graph.compile()