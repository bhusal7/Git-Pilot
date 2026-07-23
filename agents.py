from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

mistral_llm = ChatMistralAI(
    model=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
    temperature=0,
    api_key=os.getenv("MISTRAL_API_KEY"),
)

parser = StrOutputParser()

analysis_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert GitHub repository analyzer.

Write a concise markdown report.
Use the provided repository context and file list.
Always include the JSX files section if file names are provided.
Do not invent files or technologies not present in the context.
""",
        ),
        (
            "human",
            """
Question:
{query}

JSX files found locally:
{jsx_files}

Relevant repository context:
{context}

Write a clear markdown response with sections like:
- Overview
- Main files
- JSX files
- Architecture
- Notes
""",
        ),
    ]
)

analysis_chain = analysis_prompt | mistral_llm | parser