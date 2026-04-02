# Roadmap: AI Hero - RAG Course

## Milestones

- **v1.0 Day 1 - GitHub Data Ingestion** -- Phases 1-6 (shipped 2026-03-30)
- **v1.1 Day 2 - Document Chunking** -- Phases 7-12 (shipped 2026-04-01)
- **v2.0 Day 3 - Add Search** -- Phases 13-18 (current)

## Phases

<details>
<summary>v1.0 Day 1 - GitHub Data Ingestion (Phases 1-6) -- SHIPPED 2026-03-30</summary>

### Completed Phases

- [x] Phase 1: Environment Setup (1/1 plans) -- completed 2026-03-30
- [x] Phase 2: Course Project Initialization (1/1 plans) -- completed 2026-03-30
- [x] Phase 3: Core Implementation (1/1 plans) -- completed 2026-03-30
- [x] Phase 4: Course Validation (2/2 plans) -- completed 2026-03-30
- [x] Phase 5: Project Homework (1/1 plans) -- completed 2026-03-30
- [x] Phase 6: Documentation & Reflection (1/1 plans) -- completed 2026-03-30

**Total:** 7 plans completed

See [v1.0 milestone archive](milestones/1.0-ROADMAP.md) for full details.

</details>

<details>
<summary>v1.1 Day 2 - Document Chunking (Phases 7-12) -- SHIPPED 2026-04-01</summary>

### Completed Phases

- [x] Phase 7: Foundation & Dependencies (2/2 plans) -- completed 2026-03-31
- [x] Phase 8: Semantic Chunking (2/2 plans) -- completed 2026-03-31
- [x] Phase 9: LLM Chunking (1/1 plans) -- completed 2026-04-01
- [x] Phase 10: Course Notebook (1/1 plans) -- completed 2026-04-01
- [x] Phase 11: Project Homework (1/1 plans) -- completed 2026-04-01
- [x] Phase 12: Documentation & Synthesis (1/1 plans) -- completed 2026-04-01

**Total:** 8 plans completed

See [v1.1 milestone archive](milestones/1.1-ROADMAP.md) for full details.

</details>

---

## v2.0 Day 3 - Add Search (Current)

**Goal:** Build a working search system combining lexical and semantic approaches to enable efficient information retrieval from prepared documents.

**Phases:** 6 (Phases 13-18)

- [x] **Phase 13: Dependencies & Setup** - Install search libraries and establish embedding cache infrastructure (completed 2026-04-02)
- [ ] **Phase 14: Text Search Foundation** - Implement lexical search with TF-IDF scoring and field boosting
- [ ] **Phase 15: Vector Search Integration** - Add semantic search with embeddings and cosine similarity
- [ ] **Phase 16: Hybrid Search via RRF** - Combine text and vector results using Reciprocal Rank Fusion
- [ ] **Phase 17: OWASP Application & Analysis** - Apply all search methods to OWASP corpus with domain validation
- [ ] **Phase 18: Documentation & Code Quality** - Add type hints, docstrings, and learnings documentation

---

## Phase Details

### Phase 13: Dependencies & Setup
**Goal:** Install search libraries and establish embedding cache infrastructure

**Depends on:** Phase 12 (Day 2 chunking complete)

**Requirements:** DEP-04, DEP-05, DEP-06, DEP-07

**Success Criteria** (what must be TRUE):
1. User can import minsearch library for text and vector search operations
2. User can import sentence-transformers with all-MiniLM-L6-v2 model (384-dim embeddings)
3. User can verify torch backend installed for sentence-transformers (CPU-only)
4. User can see updated pyproject.toml with all new dependencies pinned to exact versions

**Plans:** 1/1 plans complete

Plans:
- [x] 13-01-PLAN.md - Install minsearch, sentence-transformers, torch and regenerate requirements.lock

---

### Phase 14: Text Search Foundation
**Goal:** Implement lexical search with TF-IDF scoring and field boosting

**Depends on:** Phase 13

**Requirements:** SEARCH-01, SEARCH-02, SEARCH-03, SEARCH-04, SEARCH-05, ORG-01, ORG-02, ORG-03, COURSE-07, COURSE-08

**Success Criteria** (what must be TRUE):
1. User can index chunked documents with minsearch.Index using TF-IDF scoring
2. User can search with configurable field boosting (title, description, content)
3. User can retrieve top-K results with relevance scores and full metadata
4. User can run text search on DataTalksClub FAQ with example queries showing exact matching
5. User can execute course/day3.ipynb from fresh kernel showing text search examples

**Plans:** TBD

**UI hint:** yes

---

### Phase 15: Vector Search Integration
**Goal:** Add semantic search with embeddings and cosine similarity

**Depends on:** Phase 14

**Requirements:** SEARCH-06, SEARCH-07, SEARCH-08, SEARCH-09, SEARCH-10, SEARCH-11, COURSE-09

**Success Criteria** (what must be TRUE):
1. User can generate embeddings for chunked documents with progress tracking (tqdm)
2. User can load cached embeddings from disk (.npy format) to avoid recomputation
3. User can create minsearch.VectorSearch index with pre-computed embeddings
4. User can search semantically with cosine similarity returning top-K results with scores
5. User can run vector search on Evidently docs with semantic queries showing conceptual matching

**Plans:** TBD

**UI hint:** yes

---

### Phase 16: Hybrid Search via RRF
**Goal:** Combine text and vector results using Reciprocal Rank Fusion

**Depends on:** Phase 15

**Requirements:** SEARCH-12, SEARCH-13, SEARCH-14, SEARCH-15, ORG-04, COURSE-10, COURSE-11, COURSE-12

**Success Criteria** (what must be TRUE):
1. User can run hybrid search combining text and vector results with RRF (k=60)
2. User can see deduplicated results by chunk_id with unified scoring
3. User can compare all three approaches side-by-side on same queries
4. User can review documented search strategy selection framework (when to use each approach)

**Plans:** TBD

---

### Phase 17: OWASP Application & Analysis
**Goal:** Apply all search methods to OWASP corpus with domain validation

**Depends on:** Phase 16

**Requirements:** HOMEWORK-01, HOMEWORK-02, HOMEWORK-03, HOMEWORK-04, HOMEWORK-05, HOMEWORK-06, HOMEWORK-07, HOMEWORK-08, HOMEWORK-09, HOMEWORK-10, HOMEWORK-11

**Success Criteria** (what must be TRUE):
1. User can index all 542 OWASP documents with text, vector, and hybrid search
2. User can test acronym handling (LLM01-10, CVE-IDs) across all three search methods
3. User can manually inspect search results for each strategy (relevance, precision intuition)
4. User can review documented analysis of which approach works best for security documentation and why
5. User can see engineering standards applied (type hints, docstrings) to all search functions

**Plans:** TBD

**UI hint:** yes

---

### Phase 18: Documentation & Code Quality
**Goal:** Add type hints, docstrings, and learnings documentation

**Depends on:** Phase 17

**Requirements:** (Addresses engineering standards across all prior work)

**Success Criteria** (what must be TRUE):
1. User can see Google-style docstrings on all search functions (purpose, Args, Returns)
2. User can find type hints on all function signatures in both notebooks
3. User can read code comments explaining tradeoffs and key decisions
4. User can execute notebooks from fresh kernel with clean, reproducible outputs

**Plans:** TBD

---

## Progress

| Phase | Milestone | Plans Complete | Status      | Completed  |
|-------|-----------|----------------|-------------|------------|
| 1-6   | v1.0      | 7/7            | Complete    | 2026-03-30 |
| 7-12  | v1.1      | 8/8            | Complete    | 2026-04-01 |
| 13    | v2.0      | 1/1 | Complete   | 2026-04-02 |
| 14    | v2.0      | 0/0            | Not started | --         |
| 15    | v2.0      | 0/0            | Not started | --         |
| 16    | v2.0      | 0/0            | Not started | --         |
| 17    | v2.0      | 0/0            | Not started | --         |
| 18    | v2.0      | 0/0            | Not started | --         |

---

## Next Steps

Run `/gsd:execute-phase 13` to execute Phase 13 plan.

---

*For historical milestones, see [MILESTONES.md](MILESTONES.md)*
