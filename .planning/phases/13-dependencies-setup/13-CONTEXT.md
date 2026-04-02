# Phase 13: Dependencies & Setup - Context

**Gathered:** 2026-04-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Install search libraries (minsearch, sentence-transformers with all-MiniLM-L6-v2, torch) and establish embedding cache infrastructure. This phase prepares the technical foundation for text search (Phase 14), vector search (Phase 15), and hybrid search (Phase 16).

**Scope:** Dependency installation only. No search implementation yet - that begins in Phase 14.

</domain>

<decisions>
## Implementation Decisions

### Dependency Versions (from Research)
- **D-01:** Use minsearch==0.0.10 (course-specified library, Feb 2026 release, Python 3.13 compatible)
- **D-02:** Use sentence-transformers==5.3.0 (Hugging Face standard, March 2026 release, includes all-MiniLM-L6-v2 model support)
- **D-03:** Use torch>=2.0.0 (PyTorch backend for sentence-transformers, CPU-only sufficient per research)
- **D-04:** Apply exact version pins with == for minsearch and sentence-transformers (reproducibility pattern from Phase 7)
- **D-05:** Use minimum version >=2.0.0 for torch (flexibility for minor/patch updates, stable major version)

### Installation Scope
- **D-06:** Add dependencies to BOTH course/ and project/ pyproject.toml (same dependencies in both contexts)
- **D-07:** Regenerate requirements.lock in both folders after adding dependencies (follows Phase 7 pattern)
- **D-08:** Use `uv add` command for dependency installation (uv package manager from v1.0-v1.1)

### Embedding Cache Infrastructure
- **D-09:** Store embedding cache in `data/embeddings/` directory (visible, easy to inspect/delete, standard for course learning)
- **D-10:** Create data/embeddings/ directory structure in Phase 15 when embeddings are first generated (not in this phase)
- **D-11:** Cache files use .npy format (numpy arrays, per research recommendation)

### Claude's Discretion
- Exact torch version within >=2.0.0 range (e.g., 2.5.0 current stable)
- Order of dependency installation (all at once or one-by-one)
- Whether to verify model download works as part of this phase or defer to Phase 15

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Project vision, prior decisions from v1.0/v1.1
- `.planning/REQUIREMENTS.md` — DEP-04 through DEP-07 requirements for this phase
- `.planning/research/SUMMARY.md` — Stack recommendations, versions, integration patterns

### Existing Patterns (from v1.1)
- `course/pyproject.toml` — Dependency format from Day 1/Day 2
- `project/pyproject.toml` — Engineering context dependency format
- `course/requirements.lock` — Hash-pinned lockfile pattern from Phase 7
- `project/requirements.lock` — Hash-pinned lockfile pattern from Phase 7

**No external specs** — requirements fully captured in decisions above and research documentation.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Patterns
- **uv workflow**: Phase 1-7 established `uv add` → `uv sync` pattern for dependency management
- **Exact version pins**: Phase 7 precedent using `==` for primary dependencies (tiktoken==0.12.0, openai==2.30.0, groq==1.1.2)
- **Dual context sync**: Both course/ and project/ get same dependencies with same versions

### Integration Points
- **pyproject.toml location**: `course/pyproject.toml` and `project/pyproject.toml` (separate uv projects)
- **requirements.lock generation**: `uv pip compile pyproject.toml --generate-hashes --output-file requirements.lock` (from v1.1 completion)
- **Pre-commit hooks**: project/.pre-commit-config.yaml will run pip-audit on new dependencies (added in v1.1)

### Established Constraints
- **Python 3.13**: Both contexts use Python 3.13 (set in Phases 2, 5)
- **No GPU dependencies**: Research confirms CPU-only torch sufficient for course scale
- **In-memory processing**: No database or persistent storage infrastructure needed (pattern from Day 1/Day 2)

</code_context>

<specifics>
## Specific Ideas

**Research-backed choices:**
- all-MiniLM-L6-v2 model: 384-dim vectors, 22MB size, 14.7ms/1K tokens CPU inference, 84-85% accuracy on STS-B benchmark
- minsearch wraps scikit-learn TF-IDF (not BM25, but acceptable for course per research)
- Embedding cache reduces recomputation from ~60s to <1s reload time (critical for course workflow)

**From Day 3 course materials:**
- sentence-transformers specified by course as standard for semantic search
- Model choice (all-MiniLM-L6-v2) balances speed vs accuracy for learning objectives

</specifics>

<deferred>
## Deferred Ideas

**Future optimizations (Day 4-7 or production):**
- GPU acceleration (requires torch with CUDA, deferred per research)
- BM25S library upgrade (500x faster than minsearch, but course uses minsearch)
- FastEmbed (ONNX-based, 4-5x faster but less model support)
- Vector databases (Chroma, FAISS, Qdrant - premature for 542 OWASP docs per research)

None — discussion stayed within phase scope (dependency installation only).

</deferred>

---

*Phase: 13-dependencies-setup*
*Context gathered: 2026-04-01*
