# Phase 7: Sliding Window Chunking Flow

```mermaid
flowchart TD
    Start([Input: Document with metadata]) --> LoadDoc[Load document text and metadata]
    LoadDoc --> InitParams[Initialize chunking parameters<br/>chunk_size=2000, overlap=1000]

    InitParams --> CheckEmpty{Text empty?}
    CheckEmpty -->|Yes| ReturnEmpty[Return empty list]
    CheckEmpty -->|No| InitVars[Initialize:<br/>chunks = []<br/>start_pos = 0]

    InitVars --> LoopCheck{start_pos < text_length?}
    LoopCheck -->|No| ReturnChunks[Return chunks list]
    LoopCheck -->|Yes| ExtractChunk[Extract chunk:<br/>text[start_pos : start_pos + chunk_size]]

    ExtractChunk --> CreateMeta[Create chunk metadata:<br/>- chunk_id<br/>- chunk_index<br/>- total_chunks (estimated)<br/>- chunk_method='sliding_window']

    CreateMeta --> PreserveMeta[Preserve original metadata:<br/>- filename<br/>- frontmatter fields]

    PreserveMeta --> CountTokens[Count tokens using tiktoken<br/>encoding=cl100k_base]

    CountTokens --> AddToList[Add chunk dict to chunks list]

    AddToList --> CalcNext[Calculate next position:<br/>start_pos += chunk_size - overlap]

    CalcNext --> LoopCheck

    ReturnChunks --> End([Output: List of chunk dicts<br/>with metadata and token counts])
    ReturnEmpty --> End

    style Start fill:#e1f5fe
    style End fill:#e1f5fe
    style CountTokens fill:#fff9c4
    style PreserveMeta fill:#fff9c4
```

## Key Transformations

**Input:**
```python
{
    "filename": "docs/guide.md",
    "content": "Long text content...",
    "title": "User Guide",
    # ... other frontmatter fields
}
```

**Output:**
```python
[
    {
        "filename": "docs/guide.md",
        "content": "Long text content... (first 2000 chars)",
        "title": "User Guide",
        "chunk_id": "docs/guide.md#chunk-0",
        "chunk_index": 0,
        "total_chunks": 5,
        "chunk_method": "sliding_window",
        "token_count": 553,
        # ... preserved frontmatter fields
    },
    {
        "filename": "docs/guide.md",
        "content": "... (chars 1000-3000, with overlap)",
        "title": "User Guide",
        "chunk_id": "docs/guide.md#chunk-1",
        "chunk_index": 1,
        "total_chunks": 5,
        "chunk_method": "sliding_window",
        "token_count": 547,
        # ... preserved frontmatter fields
    },
    # ... more chunks
]
```

## Dependencies Introduced

- `tiktoken==0.12.0` - Token counting for accurate chunk sizing
- `openai==2.30.0` - API access for future LLM chunking (Phase 9)
- `groq==1.1.2` - Alternative LLM provider with free tier

## Metadata Preservation Strategy

All Day 1 metadata fields are preserved across all chunks:
- Original filename
- YAML frontmatter fields (title, tags, etc.)
- New chunk-specific fields added without overwriting originals
- Deep copy used to prevent mutation of source documents
