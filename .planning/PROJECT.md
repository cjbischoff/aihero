# AI Hero - RAG Course Project

## What This Is

A hands-on course project following the AI Hero crash course on building intelligent systems that understand and interact with data. Day 1 delivered a working GitHub data ingestion system that downloads repositories and extracts structured markdown documentation with frontmatter metadata.

The end goal is a conversational agent that can answer questions about any GitHub repository - similar to DeepWiki but tailored to GitHub repos. This project focuses on learning RAG (Retrieval Augmented Generation) patterns through practical implementation.

## Core Value

Build working RAG pipeline components step-by-step, understanding each stage from data ingestion through conversational agents.

## Requirements

### Validated

**Day 1: GitHub Data Ingestion** — v1.0
- ✓ Set up uv project structure in `course/` and `project/` subfolders
- ✓ Install required dependencies (requests, python-frontmatter, jupyter)
- ✓ Implement `read_repo_data()` function that downloads GitHub repos as zip archives
- ✓ Parse markdown files (.md and .mdx) with frontmatter metadata
- ✓ Test with DataTalks.Club FAQ repository (1,285 docs)
- ✓ Test with Evidently AI docs repository (95 docs)
- ✓ Test with OWASP LLM Top 10 repository (542 docs)
- ✓ Create working Jupyter notebooks demonstrating functionality
- ✓ Include explanations of key concepts (frontmatter parsing, zip handling, in-memory processing)
- ✓ Set up engineering standards in `project/` folder with pre-commit hooks
- ✓ Add CodeRabbit CLI for automated code review

### Active

**Day 3: Vector Embeddings & Search (v2.0 - Planning)**
- [ ] TBD - Define requirements in next milestone cycle

### Out of Scope

**Future Course Days (defer to subsequent milestones):**
- Day 2: Document chunking for large files
- Day 3+: Search engine integration
- Day 4+: Conversational agent implementation
- Production deployment
- Custom UI/web interface
- Authentication or multi-user support

**Not in Course Scope:**
- Production-grade error handling and monitoring
- Comprehensive test suite (unit/integration/e2e)
- Security hardening (semgrep, snyk, bandit)
- CI/CD pipeline
- Performance optimization for large repos

## Current State

**Shipped:**
- v1.0 Day 1 - GitHub Data Ingestion (2026-03-30)
- v1.1 Day 2 - Document Chunking (2026-04-01)

**Codebase:**
- 2 uv projects: `course/` (learning) and `project/` (engineering standards)
- 3 working Jupyter notebooks: day1.ipynb, day2.ipynb, owasp_homework.ipynb
- Tech stack: Python 3.13, uv, requests, python-frontmatter, jupyter, tiktoken, openai, groq
- Pre-commit hooks: ruff, black, mypy, bandit, snyk, CodeRabbit CLI

**What Works:**
- Downloads any public GitHub repository as zip archive
- Extracts markdown documentation (.md and .mdx files)
- Parses YAML frontmatter metadata (gracefully handles files without it)
- Processes everything in-memory (no disk I/O)
- Returns structured data ready for RAG indexing
- Four chunking strategies: sliding window, paragraph-based, section-based, LLM-based
- Hybrid chunking combining paragraph boundaries with sliding window
- Token counting infrastructure with tiktoken
- Comparison framework for evaluating chunking strategies

**Validated Patterns:**
- In-memory zip processing with BytesIO
- Frontmatter-based metadata extraction
- Separation of course-quality (learning) vs engineering-quality (production) code
- Engineering standards: GPG signing, pre-commit hooks, CodeRabbit review
- Multi-strategy chunking with comparison frameworks
- Cost-aware LLM chunking with provider switching

## Next Milestone Goals

**v2.0 Day 3 - Vector Embeddings & Search** (Planning)
- Define requirements for embedding generation
- Vector database integration
- Semantic search implementation
- Retrieval quality metrics

## Context

**Learning Context:**
- Following AI Hero email course structure
- Building foundational understanding of RAG systems
- Each day builds on previous work (ingestion → chunking → indexing → agent)
- Day 1 validated with 3 different repositories showing pattern universality

**Technical Background:**
- GitHub repos often use frontmatter format for documentation (Jekyll, Hugo, Next.js)
- Frontmatter is YAML metadata between `---` markers at the start of markdown files
- Processing happens in-memory (no disk I/O for downloaded zips)
- python-frontmatter library gracefully handles files without metadata
- OWASP repo (539/542 files without frontmatter) proved robustness

**Repo Structure:**
```
aihero/
├── course/              # Course reproductions (learning focus)
│   ├── pyproject.toml   # uv project configuration
│   ├── day1.ipynb       # Day 1 implementation with DataTalks/Evidently tests
│   └── README.md        # Course-specific documentation
├── project/             # Personal implementations (engineering focus)
│   ├── pyproject.toml   # uv with dev dependencies
│   ├── .pre-commit-config.yaml  # Quality gates
│   ├── owasp_homework.ipynb     # OWASP LLM Top 10 analysis
│   └── README.md        # Engineering standards documentation
├── docs/                # Diagrams and documentation
│   └── diagrams/        # Mermaid flowcharts (e.g., github-ingestion-pipeline.md)
├── README.md            # Project overview and setup
└── .planning/           # GSD planning artifacts (gitignored)
```

## Constraints

- **Python Version**: 3.10 or higher (course requirement)
- **Package Manager**: uv (modern, fast alternative to pip/poetry)
- **Code Quality**: Course-quality code (learning focus, not production)
  - Jupyter notebooks are primary artifacts
  - Basic error handling sufficient
  - No need for comprehensive tests or security scans
  - Engineering standards in CLAUDE.md apply to future `project/` folder, not `course/`
- **Dependencies**: Minimal - only what course specifies (requests, python-frontmatter, jupyter)
- **Learning Style**: Implement with explanations - understand concepts, don't just copy code

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use uv instead of pip/poetry | Course requirement, modern package manager with better performance | ✓ Good — fast, reliable |
| Process zips in-memory | More efficient than disk I/O, course pattern | ✓ Good — works for repos up to 320MB |
| Course-quality over production | Focus on learning RAG concepts, not engineering rigor | ✓ Good — clear separation achieved |
| Separate course/ and project/ folders | Course reproductions vs personal implementations | ✓ Good — enables engineering standards in project/ only |
| Use Python 3.13 | Match course environment | ⚠️ Revisit — semgrep incompatible, consider 3.12 for next milestone |
| CodeRabbit CLI for pre-push review | Automated quality gate before push | ✓ Good — caught 16 issues before merge |
| GitHub codeload API | No authentication required for public repos | ✓ Good — simple, reliable |
| Frontmatter-optional design | Handle repos with or without YAML metadata | ✓ Good — OWASP test proved universality |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-01 — Completed v1.1 milestone (Day 2)*
