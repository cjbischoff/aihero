# Project: OWASP LLM Top 10 - Engineering Implementation

> **Note:** This folder contains engineering-quality implementations of course homework (Days 1-5) applied to OWASP LLM Top 10. For production deployment code (Day 6), see the `app/` folder at the repository root. The app/ folder demonstrates the transition from notebooks to deployed modules.

This folder contains engineering-quality implementations of Days 1-5 course work applied to the OWASP LLM Top 10 repository. Includes production-grade Python modules for evaluation (Phase 25-27) with full engineering standards (type hints, docstrings, pre-commit hooks, 10/10 test coverage).

## Notebook: owasp_homework.ipynb

### What It Contains

**Day 1: GitHub Data Ingestion**
- Applies `read_repo_data()` to OWASP repository
- 542 markdown documents with nested folder structure
- Handles documents with NO frontmatter (539 of 542 files)
- Tests pipeline adaptability across different documentation conventions

**Day 2: Document Chunking**
- All four chunking strategies tested on OWASP corpus
- Hybrid chunking implementation (paragraph + sliding window)
- Strategy comparison with quantitative metrics
- OWASP-specific analysis and recommendations

**Day 3: Search Methods**
- Text search with TF-IDF and field boosting
- Vector search with sentence embeddings
- Hybrid search with RRF fusion (k=60)
- Multi-granularity search (section chunks for text, paragraph for vector)
- 5 query experiments demonstrating search method strengths
- Analysis Summary with production recommendations

**Day 4: AI Agent for Security Documentation**
- Pydantic AI agent with OWASP-specific system prompt
- Hybrid search tool integration (RRF k=60 from Day 3)
- 8 diverse test queries covering LLM01-10, CVE references, and security concepts
- Domain-specific prompt tuning for security terminology
- Engineering standards (type hints, docstrings, inline comments)

**Day 5: LLM-as-a-Judge Evaluation System** (Phases 25-27)
- **Phase 25 (Logging)**: JSON-based agent interaction logging (`src/aihero/logging.py`)
- **Phase 26 (Test Data)**: TestTriplet schema, validation utilities, AI-powered question generation (`src/aihero/test_data.py`, `src/aihero/question_generator.py`)
- **Phase 27 (LLM-as-a-Judge)**: Structured evaluation with Pydantic schemas, seven-dimension rubrics + OWASP security extensions (`src/aihero/evaluation.py`)
- Production modules with complete type annotations and 10/10 pytest coverage (`tests/test_evaluation.py`)
- Chain-of-thought evaluation pattern (justification before verdict)
- Separate judge model (gpt-4o-mini, temp=0.0) for bias mitigation

**Repository Analyzed:**
- **OWASP/www-project-top-10-for-large-language-model-applications**
- 542 markdown documents
- Nested folder structure (2_0_vulns/, documentation/, translations/)
- Security guidelines for LLM applications (LLM01-LLM10)

### What's Different from Course

| Aspect | Course (Evidently) | Project (OWASP) |
|--------|-------------------|-----------------|
| **Day 1: Frontmatter** | Most files have it | Almost none (539/542) |
| **Day 1: Structure** | Flat/simple | Nested directories |
| **Day 1: File Count** | 95 documents | 542 documents |
| **Day 2: Best Strategy** | Varies by structure | Section chunking (clear `##` headers) |
| **Day 2: Implementation** | All 4 strategies | All 4 + hybrid approach |
| **Day 2: Analysis** | General learnings | OWASP-specific recommendations |
| **Day 3: Search Scope** | Single granularity | Multi-granularity (sections + paragraphs) |
| **Day 3: Best Method** | Hybrid (general) | Hybrid (security docs optimized) |
| **Day 3: Analysis** | General comparison | Security-specific (acronym handling, CVE-IDs) |
| **Day 4: Agent Tool** | text_search | hybrid_search (security optimized) |
| **Day 4: Prompting** | General FAQ | Security-tuned with OWASP context |
| **Day 4: Query Scope** | 5 FAQ questions | 8 security-specific queries |
| **Day 5: Implementation** | Inline in notebook | Production modules (src/aihero/) |
| **Day 5: Test Coverage** | Educational focus | 10/10 pytest coverage with type safety |
| **Day 5: Rubrics** | 7 base dimensions | 7 base + 2 OWASP security extensions |

### Key Learnings

**Day 1:**
- python-frontmatter gracefully handles missing metadata (returns empty `{}`)
- In-memory zip processing is structure-agnostic
- Good abstractions work across 95, 542, or 1,285 files

**Day 2:**
- OWASP's `## ` structure (LLM01, LLM02, etc.) ideal for section chunking
- Hybrid approach solves paragraph size variance (max 43K tokens → 547 tokens)
- Security documentation benefits from topic-aligned chunks (preserves LLM01-10 boundaries)
- Section chunking: 1,023 chunks, avg 1,045 tokens, preserves nested `###` headers

**Day 3:**
- Multi-granularity search: section chunks for text (1,023), paragraph for vector (14,254)
- Text search excels at exact acronyms (LLM01-10, CVE-IDs) critical for security docs
- Vector search handles conceptual queries ("how to secure AI models")
- Hybrid search combines both via RRF fusion (k=60) - production recommendation
- Paragraph→section mapping enables deduplication across different granularities
- Analysis Summary identifies hybrid search as optimal for security documentation

**Day 4:**
- OWASP agent uses hybrid_search as tool (optimal from Day 3 research)
- Security-focused system prompt improves relevance for LLM01-10 queries
- Domain-specific prompts: cite sources, use security terminology, reference OWASP guidelines
- Agent loop handles error cases gracefully (empty results, API failures)
- Framework benefits: ~70% code reduction vs manual OpenAI implementation

**Day 5 (Phases 25-27):**
- **Logging (Phase 25)**: JSON logging enables evaluation pipeline (session metadata, messages, response)
- **Test Data (Phase 26)**: 125 test triplets (25 manual + 100 AI-generated via Pydantic AI question generator)
- **LLM-as-a-Judge (Phase 27)**: Structured evaluation with EvaluationCheck and EvaluationChecklist Pydantic schemas
- **OWASP Extensions**: Two additional rubrics (security_correctness, cve_citation_accuracy) beyond base seven dimensions
- **Production Standards**: Complete type annotations, 10/10 pytest coverage, MyPy strict mode passing
- **Chain-of-Thought**: Field ordering (justification before check_pass) reduces evaluation variance 10-15%
- **Bias Mitigation**: Separate judge model (gpt-4o-mini) with temperature=0.0 for deterministic evaluation

**Architecture:**
- Day 1: [GitHub Ingestion Pipeline](../docs/diagrams/github-ingestion-pipeline.md)
- Day 2: [Hybrid Chunking Strategy](../docs/diagrams/hybrid-chunking-strategy.md)
- Day 3: [Text Search Foundation](../docs/diagrams/text-search-foundation.md)
- Day 3: [Vector Search Integration](../docs/diagrams/vector-search-integration.md)
- Day 3: [Hybrid Search RRF Fusion](../docs/diagrams/hybrid-search-rrf-fusion.md)
- Day 4: [Agent-Tool Architecture](../docs/diagrams/agent-tool-architecture.md)
- Day 5: [LLM-as-a-Judge Evaluation Flow](../docs/diagrams/llm-as-a-judge-evaluation-flow.md)

### Running the Notebook

**Setup:**
```bash
cd project/
uv sync
uv run jupyter notebook owasp_homework.ipynb
```

**Execution:**
- Run all cells from top to bottom (Kernel → Restart & Run All)
- Expected runtime: ~5-10 minutes first run (includes embedding generation)
  - Day 1: ~45 seconds (OWASP repo download, 320MB)
  - Day 2: ~30 seconds (chunking 542 documents)
  - Day 3: ~3-4 minutes first run (embedding generation for 14,254 paragraphs)
  - Day 3: ~30 seconds cached run (embeddings loaded from .npy file)
  - Day 4: ~30 seconds (agent queries, cached embeddings)
- Note: First download may be slow due to repo size

### Engineering Standards

Unlike `course/`, this folder applies full engineering standards:

- ✅ Type hints on all function signatures
- ✅ Google-style docstrings (Args, Returns, Raises, Examples)
- ✅ Pre-commit hooks (ruff, black, mypy, bandit, snyk, **pip-audit**)
- ✅ Hash-pinned dependencies (`requirements.lock`)
- ✅ Explicit error handling and input validation
- ✅ Engineering-grade documentation
- ✅ CodeRabbit CLI review on pre-push

See `.pre-commit-config.yaml`, `pyproject.toml`, and `requirements.lock` for toolchain configuration.

### Development Setup

**Initial Setup (after cloning):**

```bash
cd project/
uv sync                                           # Install dependencies
uv run pre-commit install                         # Install pre-commit hooks
uv run pre-commit install --hook-type pre-push    # Install pre-push hooks
```

**Code Quality Gates:**

This project has **automated quality gates** that run at different stages:

| Stage | What Runs | When It Blocks |
|-------|-----------|----------------|
| **Pre-commit** | ruff, black, mypy, bandit, snyk, pip-audit | Before commit succeeds |
| **Pre-push** | CodeRabbit CLI review | Before push completes |

**Workflow:**

1. Make changes to code
2. `git add` + `git commit`
   - Pre-commit hooks run automatically (ruff, black, mypy, bandit, snyk)
   - Fix any issues, commit succeeds ✅
3. `git push`
   - Pre-push hook runs CodeRabbit CLI review automatically
   - Reviews uncommitted changes against project standards
   - **Blocks push** if critical or major issues found ❌
   - **Allows push** if no blocking issues ✅

**CodeRabbit Review:**

- Uses `cr --plain --config ../CLAUDE.md --type uncommitted`
- Applies project engineering standards from CLAUDE.md
- Critical/major findings = blocking (must fix before push)
- Minor/nit findings = non-blocking (informational only)
- Output saved to `/tmp/cr-output.txt` for review

**Manual Review (optional):**

```bash
# Run CodeRabbit manually before committing
cr --plain --config ../CLAUDE.md --type uncommitted

# Run all pre-commit hooks manually
uv run pre-commit run --all-files
```

**Emergency Override (use sparingly):**

If CodeRabbit is down or you need to push urgently:
```bash
git push --no-verify
```

⚠️ **Warning:** This bypasses code review. Run `cr --plain --config ../CLAUDE.md` manually after pushing.

### What You'll Learn

**Day 1: Repository Adaptability**
- How the same ingestion code handles different documentation conventions
- Why frontmatter is optional (graceful degradation)
- Nested vs flat file organizations
- Designing RAG pipelines for both structured and unstructured docs

**Day 2: Chunking for Security Documentation**
- Why section chunking works best for OWASP (clear `##` structure)
- Hybrid approach solving size variance (paragraph + sliding window)
- Quantitative comparison: 3563 vs 14254 vs 1023 vs 14745 chunks
- Topic-aligned boundaries (preserves LLM01-10 security guidelines)
- Trade-offs: predictability vs structure-awareness vs cost

**Day 3: Search for Security Documentation**
- Multi-granularity search strategy (section for text, paragraph for vector)
- Why text search dominates acronym matching (LLM01-10, CVE-IDs)
- When vector search handles conceptual security queries better
- How RRF fusion (k=60) combines both methods optimally
- Paragraph→section mapping for cross-granularity deduplication
- Production recommendation: Hybrid search as default for security docs

**Day 4: Agents for Security Documentation**
- How Pydantic AI simplifies agent development
- Domain-specific system prompt engineering
- Hybrid search as agent tool (combining text + vector)
- Error handling in agent loops
- Security-focused query patterns (LLM01-10, CVEs, concepts)

**Day 5: Production Evaluation System**
- Complete evaluation pipeline (logging → test data → judge → metrics)
- Structured output with Pydantic schemas (EvaluationCheck, EvaluationChecklist)
- Multi-dimension rubrics (7 base + 2 OWASP security extensions)
- Chain-of-thought evaluation pattern (justification before verdict)
- Test data generation strategies (manual curation + AI synthesis)
- Production engineering standards (type safety, test coverage, MyPy strict)
- Bias mitigation (separate judge model, temperature=0.0)

**Engineering Rigor:**
- Full engineering standards (type hints, docstrings, pre-commit hooks)
- Hash-pinned dependencies for reproducible builds
- Vulnerability scanning with snyk and pip-audit
- Code quality gates preventing bad commits/pushes
- Complete implementation from data ingestion through search

### Comparison Output

The notebook shows:
- DataTalks FAQ: 1,285 files, most with frontmatter
- Evidently docs: 95 files, most with frontmatter
- OWASP LLM Top 10: 542 files, NO frontmatter

**Key Insight:** A production RAG system needs to handle both cases gracefully.

## Related: app/ Deployment Context

The `app/` folder at the repository root demonstrates Day 6 production deployment patterns:

```
app/
├── ingest.py          # Data loading (from course/day1.py patterns)
├── search_tools.py    # SearchTool class (dependency injection)
├── search_agent.py    # init_agent factory (from course/day4.ipynb)
├── logs.py            # JSON logging (from project/src/aihero/logging.py patterns)
├── main.py            # CLI entry point
└── app.py             # Streamlit web UI
```

**Key Difference:**
- `project/src/aihero/`: Production evaluation system (logging, test data, LLM-as-a-Judge)
- `app/`: Deployment demonstration (refactored FAQ agent for Streamlit Cloud)

Both use engineering standards (type hints, docstrings) but serve different purposes:
- project/ = Engineering homework applying course patterns to OWASP
- app/ = Production deployment of course FAQ agent

**Deployed Agent:** https://aihero-nbzqjktqedjuiq6bqjbjwn.streamlit.app/

### Next Steps

- Review "Analysis Summary" section in the notebook for Day 3 search insights
- Review Day 4 section for agent implementation with hybrid search
- **Review `src/aihero/` modules** for production evaluation system (Day 5)
- **Run tests**: `uv run pytest tests/test_evaluation.py -v` (10/10 passing)
- Compare with `../course/day4.ipynb` (FAQ agent) and `../course/day5.ipynb` (inline evaluation)
- **Explore app/ folder** for Day 6 deployment patterns (SearchTool class, init_agent factory)
- **Try the deployed agent**: https://aihero-nbzqjktqedjuiq6bqjbjwn.streamlit.app/
- Experiment with different queries to test search method trade-offs
- Run LLM-as-a-Judge evaluation on your own agent responses

---

**Note:** This folder demonstrates applying course concepts with production engineering practices. Code quality is higher than course reproduction to show real-world implementation standards (type safety, test coverage, pre-commit hooks).
