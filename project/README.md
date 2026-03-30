# Project: OWASP LLM Top 10 - Homework Application

This folder contains the homework implementation applying Day 1 course patterns to a different repository structure. The notebook demonstrates adaptability of the ingestion pipeline across diverse documentation conventions.

## Notebook: owasp_homework.ipynb

### What It Does

Applies the `read_repo_data()` pattern from the course to the OWASP LLM Top 10 repository - a security documentation project with a completely different structure and NO frontmatter.

**Repository Analyzed:**
- **OWASP/www-project-top-10-for-large-language-model-applications**
- 542 markdown documents
- Nested folder structure (2_0_vulns/, documentation/, translations/)
- Plain markdown with no YAML frontmatter (539 of 542 files)

### What's Different from Course

| Aspect | Course Repos | OWASP Repo |
|--------|-------------|------------|
| **Frontmatter** | Most files have it | Almost none (539/542) |
| **Structure** | Flat/simple | Nested directories |
| **File Count** | 95-1,285 | 542 |
| **Format** | Mixed .md/.mdx | Primarily .md |

### Key Learning

The same implementation works across all repositories because:

1. **python-frontmatter gracefully handles missing metadata** - Returns empty `{}` instead of errors
2. **In-memory zip processing is structure-agnostic** - Works regardless of folder nesting
3. **Good abstractions are universal** - Same function works for 95 or 1,285 or 542 files

**Pipeline Architecture:**
See [Data Flow Diagram](../docs/diagrams/github-ingestion-pipeline.md) for a visual representation of how the ingestion pipeline transforms GitHub repositories into structured documentation.

### Running the Notebook

**Setup:**
```bash
cd project/
uv sync
uv run jupyter notebook owasp_homework.ipynb
```

**Execution:**
- Run all cells from top to bottom (Kernel → Restart & Run All)
- Expected runtime: ~45 seconds (OWASP repo is 320MB)
- Note: First download may be slow due to repo size

### Engineering Standards

Unlike `course/`, this folder applies full engineering standards:

- ✅ Type hints on all function signatures
- ✅ Google-style docstrings
- ✅ Pre-commit hooks (ruff, black, mypy, bandit, snyk)
- ✅ Explicit error handling
- ✅ Engineering-grade documentation

See `.pre-commit-config.yaml` and `pyproject.toml` for toolchain configuration.

### What You'll Learn

**Repository Adaptability:**
How the same ingestion code handles:
- Different documentation conventions
- Varying levels of metadata structure
- Nested vs flat file organizations

**Frontmatter Optional:**
Why the implementation doesn't break when frontmatter is absent and how to design RAG pipelines for both structured (frontmatter) and unstructured (plain markdown) documentation.

**RAG Implications:**
- Some repos provide rich metadata out of the box
- Others require metadata extraction from content structure (headers, file paths)
- Day 2 chunking strategies will differ based on available structure

### Comparison Output

The notebook shows:
- DataTalks FAQ: 1,285 files, most with frontmatter
- Evidently docs: 95 files, most with frontmatter
- OWASP LLM Top 10: 542 files, NO frontmatter

**Key Insight:** A production RAG system needs to handle both cases gracefully.

### Next Steps

- Review "What I Learned" section in the notebook for deeper insights
- Compare with `../course/day1.ipynb` to see adaptation points
- Consider how Day 2 chunking will handle repos without frontmatter

---

**Note:** This folder demonstrates applying course concepts with production engineering practices. Code quality is higher than course reproduction to show real-world implementation standards.
