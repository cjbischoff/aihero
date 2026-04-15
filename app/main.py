"""CLI entry point for FAQ agent.

This module provides command-line interface for the FAQ agent.
Full interactive loop implementation in Phase 32.

Usage:
    python main.py
"""

import asyncio
from typing import Any

from minsearch import Index

from ingest import index_data
from search_agent import init_agent
from logs import log_interaction_to_file


# D-11, D-12: Default repository hardcoded in entry point
DEFAULT_REPO_OWNER = "DataTalksClub"
DEFAULT_REPO_NAME = "faq"


def initialize_index() -> Index:
    """Initialize search index with DataTalksClub FAQ repository.

    Downloads repository, processes markdown files, and creates
    minsearch Index for text-based search.

    Returns:
        Fitted minsearch Index ready for search operations.

    Example:
        >>> index = initialize_index()
        >>> results = index.search("What is RAG?", num_results=5)
    """
    return index_data(DEFAULT_REPO_OWNER, DEFAULT_REPO_NAME)


def initialize_agent(index: Index) -> Any:
    """Initialize FAQ agent with search tool.

    Creates pydantic-ai Agent configured with:
    - OpenAI gpt-4o-mini model
    - System prompt with GitHub repository links
    - SearchTool bound to provided index

    Args:
        index: Fitted minsearch Index from initialize_index()

    Returns:
        Configured Agent ready for .run() calls.

    Example:
        >>> index = initialize_index()
        >>> agent = initialize_agent(index)
        >>> result = await agent.run("What is RAG?")
    """
    return init_agent(index, DEFAULT_REPO_OWNER, DEFAULT_REPO_NAME)


def main() -> None:
    """CLI entry point.

    Phase 32 will implement full interactive loop with:
    - while True loop accepting user input
    - asyncio.run(agent.run(user_prompt=question))
    - Response display and logging
    - Exit command handling

    For now, this is a placeholder stub.
    """
    print("FAQ Agent CLI")
    print(f"Repository: {DEFAULT_REPO_OWNER}/{DEFAULT_REPO_NAME}")
    print("Interactive loop implementation in Phase 32")
    print()
    print("To test initialization:")
    print("  index = initialize_index()")
    print("  agent = initialize_agent(index)")


if __name__ == "__main__":
    main()
