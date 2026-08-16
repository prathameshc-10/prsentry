from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.style_agent import style_agent_node
from app.github.tools import post_pr_comment


def post_review_node(state: AgentState) -> AgentState:
    body = f"🤖 **PRSentry Review**\n\n{state['final_review']}"
    post_pr_comment(
        repo_full_name=state["repo_full_name"],
        pr_number=state["pr_number"],
        token=state["installation_token"],
        body=body,
    )
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("style_agent", style_agent_node)
    graph.add_node("post_review", post_review_node)

    graph.set_entry_point("style_agent")
    graph.add_edge("style_agent", "post_review")
    graph.add_edge("post_review", END)

    return graph.compile()