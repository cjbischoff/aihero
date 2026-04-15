"""Agent initialization module for FAQ search agent.

This module provides the system prompt template and agent factory function
for creating configured pydantic-ai agents with search capabilities.
"""

from minsearch import Index
from pydantic_ai import Agent

from search_tools import SearchTool


SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions about documentation.
Use the search tool to find relevant information from the course materials before answering questions.
Always include references by citing the filename of the source material you used.
Replace it with the full path to the GitHub repository:
"https://github.com/{repo_owner}/{repo_name}/blob/main/"
Format: [LINK TITLE](FULL_GITHUB_LINK)
"""


def init_agent(
    index: Index,
    repo_owner: str,
    repo_name: str,
) -> Agent[None, str]:
    """Initialize Pydantic AI agent with search tool.

    Creates a configured agent with:
    - OpenAI gpt-4o-mini model (course specification)
    - System prompt with GitHub repository links
    - SearchTool bound to provided index

    Args:
        index: Fitted minsearch Index from ingest.index_data()
        repo_owner: GitHub username or organization (e.g., 'DataTalksClub')
        repo_name: Repository name (e.g., 'faq')

    Returns:
        Configured pydantic-ai Agent ready for .run() calls

    Example:
        >>> from ingest import index_data
        >>> index = index_data("DataTalksClub", "faq")
        >>> agent = init_agent(index, "DataTalksClub", "faq")
        >>> result = await agent.run("What is RAG?")
        >>> print(result.output)
    """
    search_tool = SearchTool(index)

    agent = Agent(
        model="openai:gpt-4o-mini",
        system_prompt=SYSTEM_PROMPT_TEMPLATE.format(
            repo_owner=repo_owner,
            repo_name=repo_name
        ),
        tools=[search_tool.search]
    )

    return agent
