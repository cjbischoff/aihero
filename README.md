# AI Hero - RAG Course (Day 1)

A hands-on implementation of Day 1 from the AI Hero crash course on building RAG (Retrieval Augmented Generation) systems. This project demonstrates how to download GitHub repositories and extract structured documentation ready for indexing.

## What This Project Contains

This repository implements a GitHub data ingestion system that:
- Downloads repositories as zip archives via the GitHub API
- Extracts markdown documentation files (.md and .mdx)
- Parses YAML frontmatter metadata
- Returns structured data ready for RAG pipelines

## Repository Structure

```
aihero/
├── course/              # Course reproduction work
│   ├── day1.ipynb       # Main implementation notebook
│   └── pyproject.toml   # Dependencies (requests, python-frontmatter, jupyter)
│
└── project/             # Homework implementation
    ├── owasp_homework.ipynb   # OWASP LLM Top 10 analysis
    └── pyproject.toml         # Same dependencies as course/
```

**course/**: Follows the AI Hero course structure, reproducing the taught patterns with DataTalks FAQ and Evidently AI docs repositories.

**project/**: Applies learned patterns to the OWASP LLM Top 10 repository, demonstrating adaptability across different documentation structures.

## Prerequisites

- **Python 3.10+** (this project uses Python 3.13)
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))

Check your setup:
```bash
python --version  # Should show 3.10 or higher
uv --version      # Should show uv is installed
```

## Getting Started

Both `course/` and `project/` are independent uv projects. Set up either or both:

### Course Implementation
```bash
cd course/
uv sync
uv run jupyter notebook day1.ipynb
```

The course notebook walks through:
1. Helper functions (download_repo_zip, parse_markdown_with_frontmatter)
2. Main read_repo_data() function
3. Tests with DataTalks FAQ (1,285 docs) and Evidently docs (95 docs)

### Project Homework
```bash
cd project/
uv sync
uv run jupyter notebook owasp_homework.ipynb
```

The project notebook demonstrates:
1. Adapting course patterns to different repository structures
2. Handling markdown files without frontmatter (OWASP has 542 files, almost none with frontmatter)
3. Documenting learnings and differences

## Key Concepts

**Frontmatter**: YAML metadata at the start of markdown files (common in Jekyll, Hugo, Next.js docs):
```yaml
---
title: Getting Started
sidebar_position: 1
---
```

**In-Memory Processing**: The implementation processes zip archives directly in memory using `BytesIO`, avoiding disk I/O overhead.

**Structured Data**: Returns a consistent format ready for RAG indexing:
```python
{
  'filename': 'path/to/doc.md',
  'metadata': {'title': 'Page Title', ...},  # Empty {} if no frontmatter
  'content': 'Markdown content...'
}
```

## What You'll Learn

By exploring the notebooks, you'll understand:
- How to download and process GitHub repositories programmatically
- Why frontmatter is useful for documentation structure
- How the same code adapts to different repository organizations
- The foundation for building RAG systems that answer questions about code

## About the Course

This project follows the [AI Hero](https://www.ai-hero.com/) crash course on building intelligent systems. Day 1 focuses on data ingestion - the foundation for retrieval-augmented generation.

**Future Days** (not in this repo yet):
- Day 2: Document chunking for large files
- Day 3+: Search/indexing with vector databases
- Day 4+: Conversational agents with LLM integration

## Notes

- **Course-quality code**: `course/` prioritizes learning over production rigor (no comprehensive tests, type hints optional)
- **Engineering standards**: `project/` applies stricter standards (type hints, docstrings, pre-commit hooks)
- **Jupyter notebooks**: The primary artifacts - all implementation is in .ipynb files with inline explanations

## Next Steps

1. Start with `course/day1.ipynb` to see the core implementation
2. Check `project/owasp_homework.ipynb` to see how patterns adapt
3. Review the "What I Learned" sections in both notebooks for key insights

---

*Last updated: 2026-03-30 | Day 1 Complete ✓*
