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
    """Interactive CLI for FAQ agent.

    Implements:
    - Synchronous loop with input()
    - Async agent execution via asyncio.run()
    - Exit keywords: exit, quit, q
    - Ctrl+C and Ctrl+D handling
    - Real-time response display
    - Structured logging of all interactions
    """
    # Welcome message (CLI-01)
    print("FAQ Agent CLI")
    print(f"Repository: {DEFAULT_REPO_OWNER}/{DEFAULT_REPO_NAME}")
    print("Type 'exit', 'quit', or 'q' to end session\n")

    # Initialize once before loop (outside while True to avoid Pitfall 4)
    print("Initializing agent...")
    index = initialize_index()
    agent = initialize_agent(index)
    print("Ready!\n")

    # Interactive loop (CLI-02)
    while True:
        try:
            # Get user input
            question = input("You: ").strip()

            # Exit keywords
            if question.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break

            # Skip empty input (Pitfall 3)
            if not question:
                continue

            # Execute agent asynchronously (CLI-03)
            result = asyncio.run(agent.run(user_prompt=question))

            # Display response (CLI-04)
            print(f"\nAgent: {result.output}\n")

            # Log interaction
            log_interaction_to_file(agent, result, source="user")

        except KeyboardInterrupt:
            # Ctrl+C handling (Pitfall 2)
            print("\n\nInterrupted. Goodbye!")
            break
        except EOFError:
            # Ctrl+D (Unix) or Ctrl+Z (Windows): End of input
            print("\n\nGoodbye!")
            break
        except Exception as e:
            # Graceful error handling - display error and continue loop
            print(f"\nError: {e}\n")
            # Loop continues, user can try again


if __name__ == "__main__":
    main()
