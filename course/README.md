# Course: Day 1 - GitHub Repository Data Ingestion

This folder contains the course reproduction for Day 1 of the AI Hero RAG crash course. The notebook demonstrates how to download GitHub repositories and extract structured documentation ready for RAG (Retrieval Augmented Generation) systems.

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
See [Pipeline Data Flow Diagram](../docs/diagrams/phase-03-data-flow.md) for a visual representation of how data transforms through the pipeline.

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

### Next Steps

After completing this notebook:
- Check `project/` folder for homework application to OWASP repository
- Day 2 (future) will cover document chunking
- Day 3 (future) will cover indexing and search

---

**Note:** This is course-quality code focused on learning concepts, not production engineering standards. See `../project/` for a version with full engineering rigor (type hints, docstrings, pre-commit hooks).
