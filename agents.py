from tools import (
    search_repository,
    clone_repository,
    read_repository_file,
    repository_summary,
    save_report,
)

from langchain.agents import create_agent

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

parser = StrOutputParser()


explain_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert GitHub Repository Analysis AI.

Explain repositories clearly.
Describe architecture, technologies, strengths,
weaknesses and possible improvements.
""",
        ),
        (
            "human",
            """
Question:
{query}

Relevant Code:
{context}
""",
        ),
    ]
)

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a senior software architect.

Review the repository analysis critically.
Point out missing information,
incorrect assumptions and improvements.
""",
        ),
        (
            "human",
            "{draft}",
        ),
    ]
)


def build_search_agent():
    return create_agent(
        model=groq_llm,
        tools=[
            search_repository,
        ],
        system_prompt="""
Search GitHub repositories and technical documentation.
Return concise and accurate search results.
""",
    )


def build_repository_agent():
    return create_agent(
        model=groq_llm,
        tools=[
            clone_repository,
            read_repository_file,
            repository_summary,
        ],
        system_prompt="""
Analyze a GitHub repository.

Clone repositories when required.

Read project files.

Explain architecture,
frameworks,
folder structure,
dependencies,
and important implementation details.

Do not try to read directories as files.
Always choose a specific file path.
""",
    )


def build_report_agent():
    return create_agent(
        model=groq_llm,
        tools=[
            save_report,
        ],
        system_prompt="""
Generate professional markdown reports
and save them using the save_report tool.
""",
    )


explain_chain = explain_prompt | groq_llm | parser

critic_chain = critic_prompt | groq_llm | parser