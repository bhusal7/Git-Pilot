from __future__ import annotations

import warnings
from pathlib import Path

from dotenv import load_dotenv
from git import Repo

from langchain_community.document_loaders import GitLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()
warnings.filterwarnings("ignore", category=DeprecationWarning)

REPO_DIR = Path("repositories")
REPO_DIR.mkdir(exist_ok=True)


def _resolve_repo_path(repo_path: str) -> str:
    repo_path = repo_path.strip()

    if repo_path.startswith(("http://", "https://")):
        repo_name = repo_path.rstrip("/").split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        clone_path = REPO_DIR / repo_name

        if not clone_path.exists():
            Repo.clone_from(repo_path, str(clone_path))

        return str(clone_path)

    return repo_path


def _load_documents(local_repo_path: str):
    last_error = None

    for branch in ("main", "master"):
        try:
            loader = GitLoader(
                repo_path=local_repo_path,
                branch=branch,
            )
            return loader.load()
        except Exception as e:
            last_error = e

    raise last_error


def list_jsx_files(repo_path: str) -> list[str]:
    repo_path = Path(repo_path)

    if not repo_path.exists():
        return []

    jsx_files = sorted(repo_path.rglob("*.jsx"))
    return [str(f.relative_to(repo_path)) for f in jsx_files]


def build_rag(repo_path: str):
    local_repo_path = _resolve_repo_path(repo_path)
    documents = _load_documents(local_repo_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=30,
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    persist_directory = f"git_db_{Path(local_repo_path).name}"

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 2},
    )

    return retriever, local_repo_path


if __name__ == "__main__":
    build_rag(
        repo_path=r"C:/Users/Acer/OneDrive/Desktop/GenAI"
    )