#!/usr/bin/env python
# coding: utf-8

# # Day 1: GitHub Repository Data Ingestion
# 
# This notebook implements a system to download GitHub repositories and extract structured documentation. This is the foundation for building a RAG (Retrieval Augmented Generation) system that can answer questions about code repositories.
# 
# ## What We're Building
# 
# A function that:
# 1. Downloads a GitHub repository as a zip archive
# 2. Extracts markdown documentation files (.md and .mdx)
# 3. Parses YAML frontmatter metadata from each file
# 4. Returns structured data ready for indexing
# 
# ## Key Concepts
# 
# **Frontmatter**: YAML metadata block at the start of markdown files, commonly used in Jekyll, Hugo, and Next.js documentation sites. Format:
# ```yaml
# ---
# title: Getting Started
# description: Introduction guide
# sidebar_position: 1
# ---
# 
# # Markdown content here
# ```
# 
# **In-Memory Processing**: We process the zip archive directly in memory (using BytesIO) rather than writing to disk, which is more efficient for our use case.

# In[1]:


# Import required libraries
import requests
from zipfile import ZipFile
from io import BytesIO, StringIO
import frontmatter
from pathlib import Path
from typing import List, Dict, Any


# ## Helper Functions
# 
# First, we'll create helper functions to handle specific parts of the workflow:
# 1. Downloading the repository as a zip archive
# 2. Filtering for markdown files only
# 3. Parsing frontmatter from markdown content

# In[2]:


def download_repo_zip(repo_owner: str, repo_name: str) -> bytes:
    """Download GitHub repository as zip archive.

    Uses GitHub's codeload API which provides repositories as zip archives
    without requiring authentication for public repos.

    Args:
        repo_owner: GitHub username or organization (e.g., 'DataTalksClub')
        repo_name: Repository name (e.g., 'faq')

    Returns:
        Binary content of zip archive

    Raises:
        requests.HTTPError: If download fails (repo not found, network error, etc.)
    """
    url = f"https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/main"
    print(f"Downloading {repo_owner}/{repo_name} from {url}")

    response = requests.get(url)
    response.raise_for_status()  # Raise exception for HTTP errors

    print(f"Downloaded {len(response.content)} bytes")
    return response.content


# In[3]:


def is_markdown_file(filename: str) -> bool:
    """Check if file is a markdown document (.md or .mdx).

    Args:
        filename: Full path to file in zip archive

    Returns:
        True if file ends with .md or .mdx
    """
    path = Path(filename)
    return path.suffix in ['.md', '.mdx']


# In[4]:


def parse_markdown_with_frontmatter(content_bytes: bytes) -> Dict[str, Any]:
    """Parse markdown file extracting frontmatter metadata and content.

    Frontmatter is YAML metadata between --- markers at file start:
    ---
    title: Page Title
    description: Page description
    ---
    # Markdown content

    Args:
        content_bytes: Raw file content as bytes

    Returns:
        Dictionary with 'metadata' (frontmatter dict) and 'content' (markdown string)
    """
    # Decode bytes to string (GitHub files are UTF-8)
    content_str = content_bytes.decode('utf-8', errors='ignore')

    # Parse using frontmatter library
    post = frontmatter.loads(content_str)

    return {
        'metadata': dict(post.metadata),  # Convert to plain dict
        'content': post.content  # Markdown content after frontmatter
    }


# ## Main Function: read_repo_data()
# 
# Now we combine the helpers into the main function that orchestrates the entire workflow:
# 1. Download repo as zip
# 2. Open zip in memory (no disk I/O)
# 3. Filter for markdown files only
# 4. Parse each markdown file's frontmatter and content
# 5. Return structured list of documents

# In[5]:


def read_repo_data(repo_owner: str, repo_name: str) -> List[Dict[str, Any]]:
    """Download GitHub repository and extract markdown documentation with metadata.

    This is the main function that orchestrates the complete workflow:
    1. Download repository as zip archive from GitHub
    2. Process zip in-memory (no disk writes)
    3. Extract only markdown files (.md, .mdx)
    4. Parse YAML frontmatter and content from each file
    5. Return structured list of documents

    Args:
        repo_owner: GitHub username or organization (e.g., 'DataTalksClub')
        repo_name: Repository name (e.g., 'faq')

    Returns:
        List of dictionaries, each containing:
        - 'filename': str - path to file within repository
        - 'metadata': dict - YAML frontmatter key-value pairs
        - 'content': str - markdown content after frontmatter

    Example:
        >>> docs = read_repo_data('DataTalksClub', 'faq')
        >>> print(f"Found {len(evidently_docs)} markdown documents")
        >>> print(f"First doc: {docs[0]['filename']}")
        >>> print(f"Metadata: {docs[0]['metadata']}")
    """
    # Step 1: Download repository as zip
    zip_content = download_repo_zip(repo_owner, repo_name)

    # Step 2: Open zip archive in memory (BytesIO creates file-like object from bytes)
    zip_file = ZipFile(BytesIO(zip_content))

    # Step 3: Get list of all files in the archive
    all_files = zip_file.namelist()
    print(f"Total files in archive: {len(all_files)}")

    # Step 4: Filter for markdown files only
    markdown_files = [f for f in all_files if is_markdown_file(f)]
    print(f"Markdown files found: {len(markdown_files)}")

    # Step 5: Process each markdown file
    documents = []
    for filename in markdown_files:
        # Read file content from zip
        file_content = zip_file.read(filename)

        # Parse frontmatter and content
        parsed = parse_markdown_with_frontmatter(file_content)

        # Create document record
        doc = {
            'filename': filename,
            'metadata': parsed['metadata'],
            'content': parsed['content']
        }
        documents.append(doc)

    print(f"Successfully processed {len(documents)} documents")
    return documents


# ## Testing the Implementation
# 
# Let's verify our implementation works by testing with a simple example. We won't run the full course test repositories yet (that's Phase 4), but we can verify the code structure is correct.
# 
# The function signature is:
# - Input: `read_repo_data(repo_owner, repo_name)`
# - Output: `List[Dict[str, Any]]` with keys: filename, metadata, content
# - Processing: Downloads zip → filters markdown → parses frontmatter → returns structured data
# 
# **Note**: Actual testing with DataTalks.Club FAQ and Evidently AI docs repositories happens in Phase 4 (Course Validation).

# In[6]:


# Function is now ready to use
# Example usage (not executed in this notebook):
#
# docs = read_repo_data('DataTalksClub', 'faq')
# for doc in docs[:3]:  # Show first 3 documents
#     print(f"File: {doc['filename']}")
#     print(f"Metadata: {doc['metadata']}")
#     print(f"Content preview: {doc['content'][:100]}...")
#     print("-" * 80)

print("✓ read_repo_data() function defined and ready for testing")
print("✓ All helper functions loaded")
print("✓ Ready to process GitHub repositories")
print("\nNext: Phase 4 will test with real repositories (DataTalks FAQ and Evidently docs)")


# ## Test Case 1: DataTalks.Club FAQ Repository
# 
# Testing with the DataTalks.Club FAQ repository - a collection of frequently asked questions from the DataTalks.Club community. This repository contains markdown files with frontmatter metadata.
# 
# Repository: https://github.com/DataTalksClub/faq

# In[7]:


# Test with DataTalks.Club FAQ repository
print("=" * 80)
print("TEST 1: DataTalks.Club FAQ Repository")
print("=" * 80)

datatalk_docs = read_repo_data("DataTalksClub", "faq")

print(f"\n✓ Successfully processed {len(datatalk_docs)} documents")
print(f"\nFirst 3 documents:")
for i, doc in enumerate(datatalk_docs[:3], 1):
    print(f"\n{i}. {doc['filename']}")
    print(f"   Metadata keys: {list(doc['metadata'].keys())}")
    print(f"   Content length: {len(doc['content'])} characters")
    if doc["metadata"]:
        print(f"   Sample metadata: {dict(list(doc['metadata'].items())[:2])}")


# ## Test Case 2: Evidently AI Documentation
# 
# Testing with the Evidently AI documentation repository - comprehensive documentation for the Evidently ML monitoring library. This repository uses MDX format and has more complex frontmatter.
# 
# Repository: https://github.com/evidentlyai/docs

# In[8]:


# Test with Evidently AI documentation repository
print("=" * 80)
print("TEST 2: Evidently AI Documentation")
print("=" * 80)

evidently_docs = read_repo_data("evidentlyai", "docs")

print(f"\n✓ Successfully processed {len(evidently_docs)} documents")
print(f"\nFirst 3 documents:")
for i, doc in enumerate(evidently_docs[:3], 1):
    print(f"\n{i}. {doc['filename']}")
    print(f"   Metadata keys: {list(doc['metadata'].keys())}")
    print(f"   Content length: {len(doc['content'])} characters")
    if doc["metadata"]:
        print(f"   Sample metadata: {dict(list(doc['metadata'].items())[:2])}")


# ## Validation Complete ✓
# 
# Both test repositories processed successfully:
# - DataTalks.Club FAQ: Community Q&A documentation
# - Evidently AI docs: Technical product documentation
# 
# The implementation correctly:
# - Downloads repositories as zip archives
# - Extracts markdown files (.md and .mdx)
# - Parses YAML frontmatter metadata
# - Returns structured data ready for RAG indexing
# 
# **Next Steps**: Phase 5 will apply these patterns to the OWASP LLM Top 10 repository for homework.

# ## Day 1 Learnings Summary
# 
# We built a GitHub repository ingestion system that forms the foundation for RAG (Retrieval Augmented Generation). Here's what we learned:
# 
# ### Core Concepts
# 
# **Frontmatter Parsing**
# Frontmatter is YAML metadata at the top of markdown files, used by static site generators like Jekyll, Hugo, and Next.js. The python-frontmatter library extracts this metadata automatically, giving us structured data (title, description, sidebar position) alongside content. This metadata is valuable for RAG because it helps categorize and filter documents during retrieval.
# 
# **In-Memory Processing**
# We process zip archives directly in memory using BytesIO rather than writing to disk. This approach is more efficient for batch processing - we avoid filesystem I/O overhead and can process the entire archive in a single pass. For larger repositories or production systems, this pattern scales better than disk-based approaches.
# 
# **Structured Data Extraction**
# Our output format (filename, metadata, content) provides a consistent structure regardless of the source repository. This consistency is critical for Day 2 (chunking) and Day 3 (indexing) - downstream processes can rely on a predictable schema.
# 
# ### Why This Matters for RAG
# 
# 1. **Document Metadata** - Frontmatter provides categorization that improves retrieval precision. A query about "getting started" can prioritize documents where `sidebar_position: 1` or `title` contains "introduction."
# 
# 2. **Universal Patterns** - The same `read_repo_data()` function works across repositories with different structures and frontmatter conventions (as proven in the project homework with OWASP).
# 
# 3. **Processing Pipeline Foundation** - This ingestion step is the first stage of a RAG pipeline: Ingest -> Chunk -> Embed -> Index -> Query -> Generate. Clean, structured ingestion makes every subsequent step easier.
# 
# ### Next Steps
# 
# Day 2 will tackle document chunking - breaking large documents into smaller pieces while preserving context. The structured data format we created here makes chunking straightforward: we can chunk by content while preserving metadata associations.
