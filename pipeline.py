from __future__ import annotations
from typing import Dict

from main import build_rag
from agents import (
    build_report_agent,
    build_repository_agent,
    build_search_agent,
    critic_chain,
    explain_chain,
)


def human_approval(step: str) -> bool:
    """
    Human In The Loop (HITL)
    """

    while True:
        choice = input(f"Approve '{step}'? (y/n): ").strip().lower()

        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False

        print("Please enter y or n")


def run_repo_analyzer(query: str, repo_path: str) -> Dict:
    state = {}

    if query.startswith(("http://", "https://")):
        retriever_query = "Explain this repository"
        analysis_query = f"Analyze this GitHub repository: {query}"
    else:
        retriever_query = query
        analysis_query = query

    retriever = build_rag(repo_path)

    docs = retriever.invoke(retriever_query)

    context = "\n\n".join(doc.page_content for doc in docs)

    state["query"] = query
    state["context"] = context

    print("=" * 60)
    print("STEP 1 : SEARCH AGENT")
    print("=" * 60)

    search_agent = build_search_agent()

    search_result = search_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": analysis_query,
                }
            ]
        }
    )

    state["search"] = search_result["messages"][-1].content

    print("=" * 60)
    print("STEP 2 : REPOSITORY AGENT")
    print("=" * 60)

    repo_agent = build_repository_agent()

    repo_result = repo_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": analysis_query,
                }
            ]
        }
    )

    state["repository"] = repo_result["messages"][-1].content

    print("=" * 60)
    print("STEP 3 : EXPLANATION")
    print("=" * 60)

    report = explain_chain.invoke(
        {
            "query": analysis_query,
            "context": context,
        }
    )

    state["report"] = report

    print("=" * 60)
    print("STEP 4 : REVIEW")
    print("=" * 60)

    feedback = critic_chain.invoke(
        {
            "draft": report,
        }
    )

    state["feedback"] = feedback

    if not human_approval("save report"):
        return state

    print("=" * 60)
    print("STEP 5 : REPORT AGENT")
    print("=" * 60)

    report_agent = build_report_agent()

    report_result = report_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Save the following GitHub repository analysis.

Filename:
github_repository_analysis

Content:
{feedback}
""",
                }
            ]
        }
    )

    state["saved_report"] = report_result["messages"][-1].content

    return state


if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("FINAL REPORT")
    print("=" * 60)

    while True:
        query = input("You: ").strip()

        if query.lower() in ["exit", "quit", "0"]:
            print("\nBot: Goodbye.")
            break

        result = run_repo_analyzer(
            query=query,
            repo_path=query,
        )

        print("Bot:")
        print("=" * 70)
        print(result.get("feedback", "No feedback generated."))
        print("=" * 70)