import ast
import os
import shutil
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

from git import Repo
from github import Github
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None
github_client = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()

REPO_DIR = Path("repositories")
REPORT_DIR = Path("reports")

REPO_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


@lru_cache(maxsize=32)
def tools_cache(query: str):
    """Cache Tavily search results."""

    if tavily_client is None:
        return {"results": []}

    return tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=3,
    )


@tool
def search_repository(query: str) -> str:
    """
    Search technical documentation using Tavily.
    """

    response = tools_cache(query)

    if not response:
        return "No response found."

    output = []

    for result in response.get("results", []):
        output.append(
            f"""
Title: {result['title']}

URL: {result['url']}

Content:
{result['content']}
"""
        )

    return "\n\n".join(output)


@tool
def clone_repository(repo_url: str) -> str:
    """
    Clone a GitHub repository locally.
    """

    repo_url = repo_url.strip()
    repo_name = repo_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    clone_path = REPO_DIR / repo_name

    if clone_path.exists():
        return f"Repository already exists:\n{clone_path}"

    try:
        Repo.clone_from(repo_url, str(clone_path))
        return f"Repository cloned successfully:\n{clone_path}"
    except Exception as e:
        return f"Unable to clone repository: {e}"


@tool
def read_repository_file(file_path: str) -> str:
    """
    Read a repository file safely.
    """

    path = Path(file_path)

    if not path.exists():
        return "File not found."

    if path.is_dir():
        available_files = [str(p) for p in list(path.iterdir())[:10]]
        return f"""
{file_path} is a directory.

Available files:
{available_files}
Please provide a specific file path.
"""

    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except Exception as e:
        return f"Unable to read file: {e}"


@tool
def repository_summary(repo_name: str) -> str:
    """
    Return GitHub repository information.
    """

    try:
        value = repo_name.strip()

        if value.startswith(("http://", "https://")):
            value = value.split("github.com/", 1)[-1].strip("/")

        parts = [part for part in value.split("/") if part]
        if len(parts) >= 2:
            value = "/".join(parts[:2])

        repo = github_client.get_repo(value)

        return f"""
Repository : {repo.full_name}

Description : {repo.description}

Language : {repo.language}

Stars : {repo.stargazers_count}

Forks : {repo.forks_count}

Open Issues : {repo.open_issues_count}

Default Branch : {repo.default_branch}
"""
    except Exception as e:
        return str(e)


@tool
def save_report(content: str, filename: str) -> str:
    """
    Save analysis report.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = REPORT_DIR / f"{filename}_{timestamp}.md"

    filepath.write_text(
        content,
        encoding="utf-8",
    )

    return f"Report saved to {filepath}"