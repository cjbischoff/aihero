#!/usr/bin/env python
# coding: utf-8

# Day 2: Document Chunking Functions
#
# Essential chunking functions extracted from day2.ipynb for cross-notebook imports.
# Provides sliding window, paragraph, and section-based chunking strategies.

import copy
import tiktoken
import re


def count_tokens(text, encoding='cl100k_base'):
    """Count tokens in text using tiktoken.

    Args:
        text: Text to count tokens for
        encoding: Tiktoken encoding (default cl100k_base for GPT-4/3.5)

    Returns:
        Number of tokens
    """
    enc = tiktoken.get_encoding(encoding)
    return len(enc.encode(text))


def chunk_sliding_window(doc, chunk_size=2000, overlap=1000):
    """Split document into overlapping chunks using sliding window.

    Args:
        doc: Document dict with 'content', 'filename', 'metadata' keys
        chunk_size: Characters per chunk (default 2000 ≈ 512 tokens)
        overlap: Characters overlap between chunks (default 1000)

    Returns:
        List of chunk dicts with preserved metadata

    Raises:
        ValueError: If required keys missing or invalid parameters
    """
    # Validation
    if 'content' not in doc or 'filename' not in doc:
        raise ValueError("Document must have 'content' and 'filename' keys")
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")

    content = doc['content']
    chunks = []
    start = 0

    while start < len(content):
        end = start + chunk_size
        chunk_content = content[start:end]

        # Create chunk with metadata preservation
        chunk = {
            'filename': doc['filename'],
            'metadata': copy.deepcopy(doc.get('metadata', {})),
            'content': chunk_content,
            'chunk_id': f"{doc['filename']}-chunk-{len(chunks)}",
            'chunk_index': len(chunks),
            'total_chunks': -1,  # Updated after loop
            'chunk_method': 'sliding_window'
        }
        chunks.append(chunk)
        start += (chunk_size - overlap)  # Slide by (size - overlap) to create overlap

    # Update total_chunks for all
    total = len(chunks)
    for chunk in chunks:
        chunk['total_chunks'] = total

    return chunks


def chunk_by_paragraph(doc):
    """Split document into paragraph chunks.

    Splits on blank lines (\\n\\s*\\n pattern), filters empty paragraphs,
    and preserves all metadata from the source document.

    Args:
        doc: Document dict with 'content', 'filename', 'metadata' keys

    Returns:
        List of chunk dicts with preserved metadata
    """
    # Split on \n\s*\n pattern - matches paragraph boundaries
    paragraphs = re.split(r'\n\s*\n', doc['content'])

    # Filter empty paragraphs created by multiple blank lines
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Create chunks with metadata preservation
    chunks = []
    for i, para_text in enumerate(paragraphs):
        chunk = {
            'filename': doc['filename'],
            'metadata': copy.deepcopy(doc.get('metadata', {})),
            'content': para_text,
            'chunk_id': f"{doc['filename']}-chunk-{i}",
            'chunk_index': i,
            'total_chunks': len(paragraphs),
            'chunk_method': 'paragraph'
        }
        chunks.append(chunk)

    return chunks


def chunk_by_section(doc):
    """Split document by ## markdown headers.

    Each chunk contains one ## section with all nested subsections
    until the next ## header. Header text is included in the chunk.

    Args:
        doc: Document dict with 'content', 'filename', 'metadata' keys

    Returns:
        List of chunk dicts with preserved metadata
    """
    # Find all ## headers and their positions
    pattern = r'^##\s+(.+)$'
    matches = list(re.finditer(pattern, doc['content'], re.MULTILINE))

    if not matches:
        # No sections found, return whole doc as single chunk
        return [{
            'filename': doc['filename'],
            'metadata': copy.deepcopy(doc.get('metadata', {})),
            'content': doc['content'],
            'chunk_id': f"{doc['filename']}-chunk-0",
            'chunk_index': 0,
            'total_chunks': 1,
            'chunk_method': 'section'
        }]

    chunks = []
    for i, match in enumerate(matches):
        start = match.start()
        # Section ends where next ## starts, or at doc end
        end = matches[i+1].start() if i+1 < len(matches) else len(doc['content'])

        section_text = doc['content'][start:end].strip()

        # Skip empty sections
        if not section_text:
            continue

        chunk = {
            'filename': doc['filename'],
            'metadata': copy.deepcopy(doc.get('metadata', {})),
            'content': section_text,  # includes header
            'chunk_id': f"{doc['filename']}-chunk-{len(chunks)}",
            'chunk_index': len(chunks),
            'total_chunks': -1,  # Updated after loop
            'chunk_method': 'section'
        }
        chunks.append(chunk)

    # Update total_chunks for all
    total = len(chunks)
    for chunk in chunks:
        chunk['total_chunks'] = total

    return chunks
