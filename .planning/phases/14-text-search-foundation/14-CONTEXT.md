# Phase 14: Text Search Foundation - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement lexical search with TF-IDF scoring using minsearch library. Index chunked documents from Day 2, enable keyword-based retrieval with relevance scoring, and demonstrate text search on course datasets (DataTalksClub FAQ, Evidently docs). This phase establishes the first of three search methods (text → vector → hybrid).

**Scope:** Text/lexical search only. No vector embeddings, no hybrid fusion - those are Phase 15 and 16 respectively.

</domain>

<decisions>
## Implementation Decisions

### Field Boosting Configuration
- **D-01:** Use moderate field boosting: title:2.0, content:1.0 (no description field in current schema)
- **D-02:** Configure boosting at index creation time (not runtime parameter)
- **D-03:** Title matches get 2x weight relative to content matches (observable in rankings, common production pattern)

### Search Function Interface
- **D-04:** text_search() signature: `text_search(query: str, top_k: int = 5) -> list[dict]`
- **D-05:** Minimal parameter surface (query and top_k only, boosting pre-configured)
- **D-06:** Return format: list of dicts with score injected: `[{"content": ..., "title": ..., "score": 0.85, "chunk_id": ..., "filename": ...}, ...]`
- **D-07:** Unified result format across text_search, vector_search, hybrid_search (requirement ORG-02)
- **D-08:** Score is float 0.0-1.0+ (TF-IDF can exceed 1.0, that's expected)

### Example Query Selection (Course Notebook)
- **D-09:** Balanced demonstration: 2-3 queries where text search excels + 1-2 where it struggles
- **D-10:** Text search strengths: exact terminology ("TF-IDF"), acronyms ("FAQ", "API"), specific names
- **D-11:** Text search limitations: paraphrases ("how to count words" → won't match "token counting"), conceptual queries
- **D-12:** Use course datasets only (DataTalksClub FAQ per SEARCH-04, Evidently docs per SEARCH-05)
- **D-13:** No OWASP queries in Phase 14 - OWASP application is Phase 17 per roadmap

### Code Organization (from Requirements)
- **D-14:** Create course/day3.ipynb following day1.ipynb and day2.ipynb patterns (COURSE-07)
- **D-15:** Import Day 1 functions (load_documents) and Day 2 functions (chunk_documents) for reproducible execution (ORG-03)
- **D-16:** Structure text_search() for future agent integration (ORG-01) - consistent signature for all search functions
- **D-17:** Use type hints and docstrings per project CLAUDE.md standards

### Data Sources (from Research)
- **D-18:** DataTalksClub FAQ: Data engineering course FAQ subset (requirement SEARCH-04)
- **D-19:** Evidently docs: Already ingested in Day 1, chunked in Day 2 (requirement SEARCH-05)
- **D-20:** Both datasets use existing Day 2 chunk format (no schema changes needed)

### Claude's Discretion
- Exact queries to demonstrate (within "balanced" framework)
- Whether to show minsearch.Index internals or treat as black box
- Order of notebook sections (index first vs search first)
- Whether to include timing/performance metrics in examples
- Top-K default value (5 is suggested but can adjust based on dataset size)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Project vision, progressive enhancement pattern
- `.planning/REQUIREMENTS.md` — SEARCH-01 through SEARCH-05, ORG-01 through ORG-03, COURSE-07, COURSE-08 requirements
- `.planning/research/SUMMARY.md` — minsearch TF-IDF details, field boosting patterns, unified schema

### Existing Patterns (from v1.0 and v1.1)
- `course/day1.ipynb` — Notebook structure, markdown explanations, code organization
- `course/day2.ipynb` — Section headers, import patterns, reproducible execution
- `course/day1.py` — Converted functions for cross-notebook imports (ORG-03 pattern)
- `project/owasp_homework.ipynb` — Homework structure (Phase 17 will extend with Day 3 section)

### Data Artifacts (from prior phases)
- Day 1 output: Ingested documents (DataTalksClub FAQ, Evidently docs)
- Day 2 output: Chunked documents with `{content, title, metadata, chunk_id, filename}` schema
- Phase 13 output: minsearch 0.0.10 installed and verified

**No external specs** — requirements fully captured in decisions above and research documentation.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Patterns
- **Notebook structure** (Day 1/Day 2): Markdown intro → imports → load data → process → demonstrate → reflect
- **Cross-notebook imports** (Day 2): `from day1 import load_documents` enables reproducible execution (ORG-03)
- **Document schema** (Day 1→Day 2): `{content, title, metadata, chunk_id, filename}` — text search adds `score` field
- **In-memory processing** (Day 1/Day 2): No database, rebuild indices from scratch, fast iteration

### Integration Points
- **Input:** Chunked documents from Day 2 (list of dicts with content, title, metadata)
- **Processing:** minsearch.Index accepts list of dicts, builds TF-IDF index
- **Output:** text_search() returns list of dicts with scores (same schema + score field)
- **Next phase:** Vector search (Phase 15) uses same input documents, different indexing

### Established Constraints
- **Python 3.13** in both course/ and project/ contexts
- **Jupyter notebooks** for course, progressive execution model
- **Type hints + docstrings** required per CLAUDE.md (project/ context, not enforced in course/)
- **No GPU dependencies** - CPU-only for all processing

</code_context>

<specifics>
## Specific Ideas

**From research (minsearch capabilities):**
- minsearch.Index supports both text and vector search (Phase 14 uses text mode only)
- TF-IDF scoring is built-in, no manual vectorization needed
- Field boosting via `boost` parameter in index creation: `{"title": 2.0, "content": 1.0}`
- Returns scores as part of result dicts automatically
- Rebuilds quickly (<1 sec for 2K chunks) so can iterate on boost values

**Example query ideas (from research):**
- **Text search wins:** "TF-IDF algorithm" (exact terminology), "DataTalksClub FAQ" (proper names), "API documentation" (acronyms)
- **Text search struggles:** "how to improve models" → won't match "fine-tuning techniques" (paraphrase), "understanding data quality" → won't match "monitoring metrics" (conceptual mismatch)

**Demonstration flow suggestion:**
1. Load and chunk documents (import from Day 1/Day 2)
2. Create minsearch.Index with field boosting
3. Run 2-3 "success" queries - show title boost effect, exact match quality
4. Run 1-2 "limitation" queries - show paraphrase failure, motivate semantic search
5. Compare results side-by-side for same query on different datasets

</specifics>

<deferred>
## Deferred Ideas

**Phase 15 (Vector Search):**
- Semantic embeddings with sentence-transformers
- Handling paraphrases and conceptual queries
- Embedding cache infrastructure (data/embeddings/ per Phase 13 D-09)

**Phase 16 (Hybrid Search):**
- RRF fusion to combine text + vector results
- Deduplication by chunk_id
- Strategy selection framework (when to use text vs vector vs hybrid)

**Phase 17 (OWASP Application):**
- OWASP-specific queries and acronym handling (LLM01-10, CVE-IDs)
- Domain validation on security documentation
- Comparison of all three search methods on technical corpus

**Phase 18 (Polish):**
- Additional type hints and docstrings
- Performance metrics and timing analysis
- Learnings documentation

**Out of scope for v2.0:**
- BM25 upgrade (minsearch uses TF-IDF, BM25 is production feature)
- Query expansion or auto-correction
- Filtering by metadata fields (not in requirements)
- Real-time indexing (batch is sufficient for course)

</deferred>

---

*Phase: 14-text-search-foundation*
*Context gathered: 2026-04-02*
