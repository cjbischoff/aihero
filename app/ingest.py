"""Data ingestion module for GitHub repository processing.

This module provides functions to download GitHub repositories, extract markdown
documentation, chunk documents for better retrieval, and create searchable indexes.
"""

import copy
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from zipfile import ZipFile

import frontmatter
import requests
import tiktoken
from minsearch import Index


def read_repo_data(repo_owner: str, repo_name: str) -> List[Dict[str, Any]]:
    """Download GitHub repository and extract markdown documentation with metadata.

    Downloads a GitHub repository as a zip archive, processes it in-memory,
    extracts only markdown files (.md, .mdx), and parses YAML frontmatter
    and content from each file.

    Args:
        repo_owner: GitHub username or organization (e.g., 'DataTalksClub')
        repo_name: Repository name (e.g., 'faq')

    Returns:
        List of dictionaries, each containing:
        - 'filename': str - path to file within repository
        - 'metadata': dict - YAML frontmatter key-value pairs
        - 'content': str - markdown content after frontmatter

    Raises:
        requests.HTTPError: If download fails (repo not found, network error, etc.)

    Example:
        >>> docs = read_repo_data('DataTalksClub', 'faq')
        >>> print(f"Found {len(docs)} markdown documents")
    """
    # Download repository as zip
    url = f"https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/main"
    print(f"Downloading {repo_owner}/{repo_name} from {url}")

    response = requests.get(url)
    response.raise_for_status()

    print(f"Downloaded {len(response.content)} bytes")

    # Open zip archive in memory
    zip_file = ZipFile(BytesIO(response.content))

    # Get all files and filter for markdown
    all_files = zip_file.namelist()
    print(f"Total files in archive: {len(all_files)}")

    markdown_files = [f for f in all_files if Path(f).suffix in ['.md', '.mdx']]
    print(f"Markdown files found: {len(markdown_files)}")

    # Process each markdown file
    documents = []
    for filename in markdown_files:
        file_content = zip_file.read(filename)

        # Parse frontmatter and content
        content_str = file_content.decode('utf-8', errors='ignore')
        post = frontmatter.loads(content_str)

        doc = {
            'filename': filename,
            'metadata': dict(post.metadata),
            'content': post.content
        }
        documents.append(doc)

    print(f"Successfully processed {len(documents)} documents")
    return documents


def sliding_window(text: str, size: int, step: int) -> List[str]:
    """Split text into overlapping chunks using token-based sliding window.

    Uses tiktoken cl100k_base encoding (GPT-4/3.5) to count tokens accurately.
    Creates overlapping chunks to preserve context at boundaries.

    Args:
        text: Text to chunk
        size: Chunk size in tokens (e.g., 2000)
        step: Step size in tokens (e.g., 1000) - smaller creates more overlap

    Returns:
        List of text chunks with overlap

    Raises:
        ValueError: If size <= 0 or step <= 0 or size < step

    Example:
        >>> chunks = sliding_window("Long text...", size=2000, step=1000)
        >>> print(f"Created {len(chunks)} overlapping chunks")
    """
    if size <= 0 or step <= 0:
        raise ValueError("size and step must be positive")
    if size < step:
        raise ValueError("size must be >= step for overlap")

    # Use tiktoken for accurate token counting
    enc = tiktoken.get_encoding('cl100k_base')
    tokens = enc.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + size
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += step

    return chunks


def chunk_documents(
    docs: List[Dict[str, Any]], size: int, step: int
) -> List[Dict[str, Any]]:
    """Apply sliding window chunking to a list of documents.

    Chunks each document's content using sliding_window() while preserving
    metadata. Each chunk includes original filename and metadata.

    Args:
        docs: List of document dicts with 'content', 'filename', 'metadata' keys
        size: Chunk size in tokens (passed to sliding_window)
        step: Step size in tokens (passed to sliding_window)

    Returns:
        Expanded list of chunked documents with metadata preserved

    Raises:
        ValueError: If required keys missing from documents

    Example:
        >>> docs = read_repo_data('DataTalksClub', 'faq')
        >>> chunked = chunk_documents(docs, size=2000, step=1000)
        >>> print(f"Expanded from {len(docs)} to {len(chunked)} chunks")
    """
    chunked_docs = []

    for doc in docs:
        if 'content' not in doc or 'filename' not in doc:
            raise ValueError("Document must have 'content' and 'filename' keys")

        content = doc['content']
        chunks = sliding_window(content, size, step)

        for i, chunk_content in enumerate(chunks):
            chunk = {
                'filename': doc['filename'],
                'metadata': copy.deepcopy(doc.get('metadata', {})),
                'content': chunk_content,
                'chunk_id': f"{doc['filename']}-chunk-{i}",
                'chunk_index': i,
                'total_chunks': len(chunks),
                'chunk_method': 'sliding_window'
            }
            chunked_docs.append(chunk)

    return chunked_docs


def index_data(
    repo_owner: str,
    repo_name: str,
    filter: Optional[Callable[[Dict[str, Any]], bool]] = None,
    chunk: bool = False,
    chunking_params: Optional[Dict[str, int]] = None,
) -> Index:
    """Index GitHub repository data with optional filtering and chunking.

    Main entry point that orchestrates the complete workflow:
    1. Download repository and extract markdown docs
    2. Optionally filter documents
    3. Optionally chunk documents for better retrieval
    4. Create and fit minsearch Index for text-based search

    Args:
        repo_owner: GitHub username or organization (e.g., 'DataTalksClub')
        repo_name: Repository name (e.g., 'faq')
        filter: Optional function to filter documents (e.g., lambda doc: 'python' in doc['filename'])
        chunk: Whether to chunk documents before indexing
        chunking_params: Chunking parameters {'size': int, 'step': int} if chunk=True
                        Defaults to {'size': 2000, 'step': 1000}

    Returns:
        Fitted minsearch Index ready for search operations

    Example:
        >>> # Default: no filtering, no chunking
        >>> index = index_data("DataTalksClub", "faq")
        >>> results = index.search("What is RAG?", num_results=5)
        >>>
        >>> # With chunking
        >>> index = index_data("DataTalksClub", "faq", chunk=True)
        >>>
        >>> # With custom chunking params
        >>> index = index_data(
        ...     "DataTalksClub", "faq",
        ...     chunk=True,
        ...     chunking_params={'size': 1000, 'step': 500}
        ... )
    """
    # Download and extract docs
    docs = read_repo_data(repo_owner, repo_name)

    # Apply optional filter
    if filter is not None:
        docs = [doc for doc in docs if filter(doc)]

    # Apply optional chunking
    if chunk:
        if chunking_params is None:
            chunking_params = {'size': 2000, 'step': 1000}
        docs = chunk_documents(docs, **chunking_params)

    # Create and fit index
    index = Index(text_fields=["content", "filename"])
    index.fit(docs)

    return index
