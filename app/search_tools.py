"""Search tool module for FAQ agent.

This module provides a SearchTool class that encapsulates a minsearch Index
for use with pydantic-ai agents. The tool follows dependency injection pattern
rather than global variables.
"""

from typing import Any, List

from minsearch import Index


class SearchTool:
    """Text-based search tool wrapping minsearch Index.

    Encapsulates search index for pydantic-ai agent tool registration.
    Each instance is bound to a specific index via dependency injection.

    Attributes:
        index: Fitted minsearch Index from ingest.index_data()

    Example:
        >>> from ingest import index_data
        >>> index = index_data("DataTalksClub", "faq")
        >>> tool = SearchTool(index)
        >>> results = tool.search("What is RAG?")
        >>> print(f"Found {len(results)} results")
    """

    def __init__(self, index: Index) -> None:
        """Initialize search tool with index.

        Args:
            index: Fitted minsearch Index from ingest.index_data()
        """
        self.index = index

    def search(self, query: str) -> List[Any]:
        """Perform a text-based search on the FAQ index.

        Args:
            query: Search query string

        Returns:
            List of up to 5 most relevant documents
        """
        return self.index.search(query, num_results=5)
