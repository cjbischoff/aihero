# AI Hero - RAG Course (Days 1 & 2)

A hands-on implementation from the AI Hero crash course on building RAG (Retrieval Augmented Generation) systems. This project demonstrates GitHub data ingestion and document chunking strategies for preparing documents for RAG pipelines.

## Current Status: v1.1 Complete ✓

**v1.0 - Day 1: GitHub Data Ingestion** (shipped 2026-03-30)
- Downloads GitHub repositories as zip archives
- Extracts markdown documentation with frontmatter metadata
- Returns structured data ready for indexing

**v1.1 - Day 2: Document Chunking** (shipped 2026-04-01)
- Four chunking strategies: sliding window, paragraph, section, LLM-based
- Hybrid approach combining paragraph boundaries with sliding window
- Token counting infrastructure with tiktoken
- Comparison framework for evaluating strategies

## Repository Structure

```
aihero/
├── course/              # Course reproduction (learning focus)
│   ├── day1.ipynb       # Day 1: GitHub data ingestion
│   ├── day2.ipynb       # Day 2: Chunking strategies
│   ├── requirements.lock # Hash-pinned dependencies
│   └── pyproject.toml   # Dependencies (requests, tiktoken, openai, groq)
│
├── project/             # Engineering-quality implementations
│   ├── owasp_homework.ipynb    # OWASP analysis (Day 1 + Day 2)
│   ├── requirements.lock       # Hash-pinned dependencies
│   ├── .pre-commit-config.yaml # Quality gates (black, ruff, mypy, snyk, pip-audit)
│   └── pyproject.toml          # Dependencies + dev tools
│
└── docs/
    └── diagrams/        # Mermaid diagrams for all phases
```

**course/**: Follows AI Hero course structure with DataTalks FAQ and Evidently AI docs as examples.

**project/**: Applies learned patterns to OWASP LLM Top 10 repository with engineering standards (type hints, docstrings, pre-commit hooks).

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

# Day 1: GitHub data ingestion
uv run jupyter notebook day1.ipynb

# Day 2: Chunking strategies
uv run jupyter notebook day2.ipynb
```

**Day 1 notebook** walks through:
1. Helper functions (download_repo_zip, parse_markdown_with_frontmatter)
2. Main read_repo_data() function
3. Tests with DataTalks FAQ (1,285 docs) and Evidently docs (95 docs)

**Day 2 notebook** implements:
1. Sliding window chunking (2000 chars, 1000 overlap)
2. Paragraph-based chunking (regex `\n\s*\n`)
3. Section-based chunking (markdown `## ` headers)
4. LLM-based intelligent chunking (OpenAI/Groq)
5. Comparison framework and quality inspection
6. Learnings summary with decision framework

### Project Homework
```bash
cd project/
uv sync
uv run jupyter notebook owasp_homework.ipynb
```

The project notebook demonstrates:
1. **Day 1:** Adapting course patterns to OWASP repository (542 docs, minimal frontmatter)
2. **Day 2:** Hybrid chunking strategy (paragraph + sliding window)
3. Strategy comparison on OWASP corpus
4. Documented analysis: which chunking approach works best for security documentation

## Key Concepts

### Day 1: Data Ingestion

**Frontmatter**: YAML metadata at the start of markdown files (common in Jekyll, Hugo, Next.js docs):
```yaml
---
title: Getting Started
sidebar_position: 1
---
```

**In-Memory Processing**: Zip archives processed in memory using `BytesIO`, avoiding disk I/O.

**Structured Data**: Consistent format ready for RAG indexing:
```python
{
  'filename': 'path/to/doc.md',
  'metadata': {'title': 'Page Title', ...},
  'content': 'Markdown content...'
}
```

### Day 2: Chunking Strategies

**Chunking**: Breaking large documents into smaller pieces for embedding and retrieval.

**Four Strategies Implemented:**

1. **Sliding Window**: Fixed-size chunks (2000 chars) with overlap (1000 chars)
   - Predictable sizes, fast
   - Ignores document structure

2. **Paragraph**: Split on double newlines (`\n\s*\n`)
   - Respects natural text boundaries
   - Variable sizes (some huge, some tiny)

3. **Section**: Split by markdown headers (`## `)
   - Topic-aligned, preserves structure
   - Requires structured markdown

4. **LLM**: Semantic boundaries using GPT/Mixtral
   - Highest quality, context-aware
   - Costs scale with corpus size

**Hybrid Approach**: Paragraph-first with sliding window fallback for oversized paragraphs. Best of both worlds.

**Token Counting**: Uses `tiktoken` (cl100k_base) for accurate token counts matching GPT-3.5/4 tokenizers.

## What You'll Learn

By exploring the notebooks, you'll understand:

**Day 1:**
- How to download and process GitHub repositories programmatically
- Why frontmatter is useful for documentation structure
- How code adapts to different repository organizations

**Day 2:**
- Trade-offs between simple vs. semantic chunking strategies
- When to use sliding window vs. paragraph vs. section vs. LLM chunking
- How to implement hybrid strategies for real-world documents
- Cost analysis for LLM-based chunking (free tiers vs. paid)
- Comparison frameworks for evaluating chunking quality

## About the Course

This project follows the [AI Hero](https://www.ai-hero.com/) crash course on building intelligent systems.

**✓ Day 1 (v1.0)**: Data ingestion - downloading and parsing GitHub documentation
**✓ Day 2 (v1.1)**: Document chunking - preparing documents for embedding and retrieval

**Future Days** (v2.0+):
- Day 3: Vector embeddings and search
- Day 4+: Conversational agents with LLM integration

## Standards & Quality

**Course Context** (`course/` folder):
- Learning-focused Jupyter notebooks
- Inline comments explaining concepts
- Reproducible from fresh kernel
- No comprehensive test suite (learning, not production)

**Project Context** (`project/` folder):
- Engineering-quality implementations
- Type hints and Google-style docstrings
- Pre-commit hooks: black, ruff, mypy, bandit, snyk, pip-audit
- Hash-pinned dependencies (`requirements.lock`)
- CodeRabbit CLI review on pre-push

See `CLAUDE.md` for complete standards documentation.

## Next Steps

1. **Start with Day 1**: `course/day1.ipynb` - GitHub data ingestion
2. **Continue with Day 2**: `course/day2.ipynb` - Four chunking strategies
3. **Review project work**: `project/owasp_homework.ipynb` - OWASP analysis
4. **Explore diagrams**: `docs/diagrams/` - Mermaid flowcharts for all phases

---

*Last updated: 2026-04-01 | v1.1 Complete ✓*
