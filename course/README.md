# Course: Days 1 & 2 - RAG Fundamentals

This folder contains course reproductions for Days 1 and 2 of the AI Hero RAG crash course:
- **Day 1:** GitHub repository data ingestion
- **Day 2:** Document chunking strategies

Both notebooks demonstrate core concepts with hands-on implementations and real-world examples.

## Notebook: day1.ipynb

### What It Does

Implements a complete GitHub ingestion pipeline:
1. Downloads repositories as zip archives via GitHub's codeload API
2. Extracts markdown documentation (.md and .mdx files)
3. Parses YAML frontmatter metadata from each file
4. Returns structured data ready for indexing

### Key Components

**Helper Functions:**
- `download_repo_zip()` - Downloads repo without authentication
- `is_markdown_file()` - Filters for .md/.mdx files
- `parse_markdown_with_frontmatter()` - Extracts metadata and content

**Main Function:**
- `read_repo_data(repo_owner, repo_name)` - Orchestrates the complete workflow

**Architecture:**
See [Pipeline Data Flow Diagram](../docs/diagrams/github-ingestion-pipeline.md) for a visual representation of how data transforms through the pipeline.

### Test Repositories

The notebook validates the implementation with two real-world repositories:

1. **DataTalks.Club FAQ** (1,285 documents)
   - Community Q&A documentation
   - Demonstrates handling of repositories with frontmatter

2. **Evidently AI Docs** (95 documents)
   - Technical product documentation
   - Uses MDX format with complex frontmatter

### Running the Notebook

**Setup:**
```bash
cd course/
uv sync
uv run jupyter notebook day1.ipynb
```

**Execution:**
- Run all cells from top to bottom (Kernel → Restart & Run All)
- Expected runtime: ~30-60 seconds (downloading test repos)
- All cells should execute without errors

### Key Concepts Explained

**Frontmatter:**
YAML metadata at the start of markdown files used by static site generators (Jekyll, Hugo, Next.js). Provides structured data like titles, descriptions, and navigation hints.

**In-Memory Processing:**
Uses BytesIO to process zip archives without disk I/O, making the pipeline more efficient for batch processing.

**Structured Output:**
Returns consistent format (`filename`, `metadata`, `content`) regardless of source repository structure.

### What You'll Learn

- How GitHub's codeload API works
- Why frontmatter is useful for documentation
- In-memory zip processing patterns
- Foundation for building RAG ingestion pipelines

## Notebook: day2.ipynb

### What It Does

Implements and compares four document chunking strategies for RAG systems:
1. **Sliding Window**: Fixed-size chunks (2000 chars) with overlap (1000 chars)
2. **Paragraph**: Splits on natural paragraph boundaries (`\n\s*\n`)
3. **Section**: Splits by markdown headers (`## `)
4. **LLM**: Semantic boundaries using OpenAI or Groq APIs

### Key Components

**Chunking Functions:**
- `chunk_sliding_window()` - Predictable fixed-size chunks
- `chunk_by_paragraph()` - Natural text boundaries
- `chunk_by_section()` - Topic-aligned via markdown structure
- `chunk_with_llm()` - AI-driven semantic chunking

**Analysis Tools:**
- `compare_chunking_strategies()` - Multi-metric comparison table
- `inspect_chunk_quality()` - Automated quality detection
- Token counting with tiktoken (cl100k_base encoding)

**Architecture:**
See `../docs/diagrams/phase-*-*.md` for visual representations of each chunking strategy.

### Test Data

Tests all strategies on Evidently AI docs from Day 1:
- 95 markdown documents
- Mix of structured and unstructured content
- Real-world complexity (code blocks, tables, headers)

### Running the Notebook

**Setup:**
```bash
cd course/
uv sync
uv run jupyter notebook day2.ipynb
```

**Dependencies:**
- tiktoken==0.12.0 (token counting)
- openai==2.30.0 (optional, for LLM chunking)
- groq==1.1.2 (optional, free tier alternative)

**Execution:**
- Requires Day 1 completion (imports `read_repo_data` from day1.py)
- LLM chunking section requires API key in `.env` (optional to run)
- Expected runtime: ~2-3 minutes (includes LLM API calls if enabled)

### Key Concepts Explained

**Chunking Trade-offs:**
- Sliding window: Fast, predictable, ignores structure
- Paragraph: Natural boundaries, variable sizes
- Section: Topic-aligned, requires structured docs
- LLM: Highest quality, costs scale with corpus

**Token Counting:**
Uses tiktoken with cl100k_base encoding (matches GPT-3.5/4 tokenizers) for accurate chunk sizing.

**Metadata Preservation:**
All strategies preserve original document metadata (filename, frontmatter) plus add chunk-specific fields (chunk_id, chunk_index, chunk_method, token_count).

### What You'll Learn

- Trade-offs between simple vs. semantic chunking
- When to use each strategy (decision framework)
- Cost analysis for LLM-based chunking
- Comparison frameworks for evaluating quality
- Hybrid approaches (combining strategies)

### Day 2 Learnings Summary

The notebook includes a comprehensive learnings summary with:
- Strategy comparison table (Best For | Pros | Cons | Cost)
- Key gotchas (cost scaling, size variance, structure requirements)
- Decision framework (when to use which strategy)

## Next Steps

After completing both notebooks:
1. Review project/owasp_homework.ipynb for hybrid chunking implementation
2. Explore docs/diagrams/ for visual flowcharts of all phases
3. Day 3 (v2.0) will cover vector embeddings and search

---

**Note:** This is course-quality code focused on learning concepts, not production engineering standards. See `../project/` for a version with full engineering rigor (type hints, docstrings, pre-commit hooks).
