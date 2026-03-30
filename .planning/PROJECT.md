# AI Hero - RAG Course Project

## What This Is

A hands-on course project following the AI Hero crash course on building intelligent systems that understand and interact with data. The end goal is a conversational agent that can answer questions about any GitHub repository - similar to DeepWiki but tailored to GitHub repos. This project focuses on learning RAG (Retrieval Augmented Generation) patterns through practical implementation.

## Core Value

Successfully implement Day 1: a working GitHub data ingestion system that downloads repositories and extracts structured documentation ready for indexing.

## Requirements

### Validated

(None yet — ship to validate)

### Active

**Day 1: GitHub Data Ingestion**
- [ ] Set up uv project structure in `course/` subfolder
- [ ] Install required dependencies (requests, python-frontmatter, jupyter)
- [ ] Implement `read_repo_data()` function that downloads GitHub repos as zip archives
- [ ] Parse markdown files (.md and .mdx) with frontmatter metadata
- [ ] Test with DataTalks.Club FAQ repository
- [ ] Test with Evidently AI docs repository
- [ ] Create working Jupyter notebook demonstrating the functionality
- [ ] Include explanations of key concepts (frontmatter parsing, zip handling, in-memory processing)

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

## Context

**Learning Context:**
- Following AI Hero email course structure
- Building foundational understanding of RAG systems
- Each day builds on previous work (ingestion → chunking → indexing → agent)
- Course provides working examples with DataTalks FAQ and Evidently docs

**Technical Background:**
- GitHub repos often use frontmatter format for documentation (Jekyll, Hugo, Next.js)
- Frontmatter is YAML metadata between `---` markers at the start of markdown files
- Processing happens in-memory (no disk I/O for downloaded zips)
- Simple documents (like FAQ) can be indexed as-is
- Large documents (like technical docs) need chunking (Day 2)

**Repo Structure:**
```
aihero/
├── course/              # Course reproductions (this milestone)
│   ├── pyproject.toml   # uv project configuration
│   ├── day1.ipynb       # Day 1 implementation notebook
│   └── ...              # Future day implementations
├── project/             # Personal project implementations (future)
├── CLAUDE.md            # Engineering standards (not applied to course/)
└── .planning/           # GSD planning artifacts
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
| Use uv instead of pip/poetry | Course requirement, modern package manager with better performance | — Pending |
| Process zips in-memory | More efficient than disk I/O, course pattern | — Pending |
| Course-quality over production | Focus on learning RAG concepts, not engineering rigor | — Pending |
| Separate course/ and project/ folders | Course reproductions vs personal implementations | — Pending |

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
*Last updated: 2026-03-29 after initialization*
