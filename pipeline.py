from __future__ import annotations

from pathlib import Path
from typing import Dict

from main import build_rag, list_jsx_files
from agents import analysis_chain

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


def save_report_local(filename: str, content: str) -> str:
    timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = REPORT_DIR / f"{filename}_{timestamp}.md"
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def run_repo_analyzer(query: str, repo_path: str) -> Dict:
    state = {}

    query = (query or "").strip()
    repo_path = (repo_path or "").strip()

    if not repo_path and query.startswith(("http://", "https://")):
        repo_path = query
        query = "Summarize this repository."

    retriever, local_repo_path = build_rag(repo_path)
    jsx_files = list_jsx_files(local_repo_path)

    retriever_query = query or "Summarize this repository."
    docs = retriever.invoke(retriever_query)

    if not isinstance(docs, list):
        docs = [docs]

    context = "\n\n".join(
        doc.page_content for doc in docs[:2] if hasattr(doc, "page_content")
    )

    jsx_block = (
        "\n".join(f"- {file}" for file in jsx_files)
        if jsx_files
        else "- No .jsx files found."
    )

    report = analysis_chain.invoke(
        {
            "query": retriever_query,
            "context": context,
            "jsx_files": jsx_block,
        }
    )

    saved_path = save_report_local(Path(local_repo_path).name, report)

    state["query"] = query
    state["repo_path"] = local_repo_path
    state["jsx_files"] = jsx_files
    state["context"] = context
    state["report"] = report
    state["feedback"] = report
    state["saved_report"] = f"Report saved to {saved_path}"

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