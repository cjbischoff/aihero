# Requirements: AI Hero - Day 2

**Defined:** 2026-03-30
**Core Value:** Implement and compare multiple chunking strategies to prepare large documents for RAG systems.

## v1.1 Requirements

Requirements for Day 2 completion. Each maps to roadmap phases.

### Chunking Strategies

- [x] **CHUNK-01**: Implement sliding window chunking with configurable size and overlap (default 2000 chars, 1000 overlap)
- [x] **CHUNK-02**: Implement paragraph-based chunking using regex (`\n\s*\n` pattern)
- [x] **CHUNK-03**: Implement section-based chunking by markdown headers (level 2)
- [x] **CHUNK-04**: Implement LLM-based intelligent chunking using OpenAI or Groq
- [x] **CHUNK-05**: All strategies preserve metadata (filename, frontmatter, headers)

### Supporting Features

- [x] **SUPPORT-01**: Integrate tiktoken for accurate token counting
- [x] **SUPPORT-02**: Create strategy comparison framework (chunk counts, sizes, distribution)
- [x] **SUPPORT-03**: Implement metadata preservation across all chunking strategies
- [x] **SUPPORT-04**: Provide helper functions for manual inspection and analysis of chunk quality

### Course Notebook (course/day2.ipynb)

- [x] **COURSE-01**: Create new `course/day2.ipynb` notebook (follows day1.ipynb pattern)
- [x] **COURSE-02**: Implement all four chunking strategies in notebook cells
- [x] **COURSE-03**: Test all strategies on Evidently docs from Day 1 ingestion
- [x] **COURSE-04**: Display sample outputs showing chunk structure for each strategy
- [x] **COURSE-05**: Include inline explanations of token counting, overlap rationale, and semantic boundaries
- [x] **COURSE-06**: Document learnings about when to use each chunking approach

### Project Homework (project/owasp_homework.ipynb)

- [x] **PROJ-01**: Extend existing `project/owasp_homework.ipynb` with Day 2 section *(pre-existing)*
- [x] **PROJ-02**: Add section header `## Day 2: Chunking` to delineate new work *(pre-existing)*
- [x] **PROJ-03**: Apply simple sliding window chunking to OWASP docs from Day 1 *(pre-existing)*
- [x] **PROJ-04**: Experiment with paragraph chunking + sliding window combination *(Phase 11)*
- [x] **PROJ-05**: Apply section-based chunking using markdown headers *(pre-existing)*
- [x] **PROJ-06**: Manually inspect chunk results for each strategy *(pre-existing)*
- [x] **PROJ-07**: Document analysis of which chunking strategy works best for OWASP structure and why *(Phase 11)*
- [x] **PROJ-08**: Include engineering standards (type hints, docstrings) in chunking functions *(pre-existing)*

### Dependencies

- [x] **DEP-01**: Add tiktoken to project dependencies
- [x] **DEP-02**: Add openai SDK to optional dependencies (for LLM chunking demo)
- [x] **DEP-03**: Add groq SDK as alternative to OpenAI (optional, free tier available)
- [x] **DEP-04**: Update pyproject.toml with new dependencies

### Documentation

- [ ] **DOC-01**: Document course material learnings in `course/day2.ipynb`
- [ ] **DOC-02**: Document OWASP-specific findings in `project/owasp_homework.ipynb`
- [ ] **DOC-03**: Include code comments explaining chunking strategy tradeoffs

## v2 Requirements

Deferred to future course days (Day 3+).

### Evaluation & Testing

- **EVAL-01**: Create labeled test set for retrieval quality measurement
- **EVAL-02**: Implement retrieval metrics (MRR, NDCG@k, Recall@k)
- **EVAL-03**: Automated chunk quality scoring

### Advanced Chunking

- **ADV-01**: Semantic chunking with embeddings (2026 research shows lower accuracy than simple methods)
- **ADV-02**: Hybrid retrieval preparation (dense + sparse vectors)
- **ADV-03**: Agentic chunking (experimental, not production-ready)

### Embeddings & Indexing (Day 3+)

- **EMBED-01**: Generate embeddings for chunks
- **INDEX-01**: Vector database integration
- **SEARCH-01**: Semantic search implementation

## Out of Scope

Explicitly excluded from Day 2. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Vector embeddings | Day 3 topic - requires chunking to be complete first |
| Vector database setup | Day 3 topic - search and indexing |
| Retrieval quality metrics | Day 3+ topic - requires embedding and search first |
| Production error handling | Course focuses on learning, not production quality |
| Semantic chunking frameworks (LangChain) | Research shows overkill (39MB+) for course learning; custom 20-line implementations preferred |
| NLP frameworks (NLTK, spaCy) | Unnecessary overhead (3.8MB-500MB+) for simple chunking; regex and tiktoken sufficient |
| Comprehensive testing | Course-quality code, not production-grade |
| Cost optimization beyond basics | Course demonstrates concepts; production optimization deferred |
| Deduplication of overlapping chunks | Day 3 topic before embedding (prevents storage bloat) |
| Test set creation for evaluation | Day 3+ topic when retrieval quality becomes measurable |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| **Chunking Strategies** | | |
| CHUNK-01 | 7 | Complete |
| CHUNK-02 | 8 | Complete |
| CHUNK-03 | 8 | Complete |
| CHUNK-04 | 9 | Complete |
| CHUNK-05 | 7 | Complete |
| **Supporting Features** | | |
| SUPPORT-01 | 7 | Complete |
| SUPPORT-02 | 8 | Complete |
| SUPPORT-03 | 7 | Complete |
| SUPPORT-04 | 8 | Complete |
| **Course Notebook** | | |
| COURSE-01 | 10 | Complete |
| COURSE-02 | 10 | Complete |
| COURSE-03 | 10 | Complete |
| COURSE-04 | 10 | Complete |
| COURSE-05 | 10 | Complete |
| COURSE-06 | 10 | Complete |
| **Project Homework** | | |
| PROJ-01 | 11 | Complete (pre-existing) |
| PROJ-02 | 11 | Complete (pre-existing) |
| PROJ-03 | 11 | Complete (pre-existing) |
| PROJ-04 | 11 | Complete (Phase 11) |
| PROJ-05 | 11 | Complete (pre-existing) |
| PROJ-06 | 11 | Complete (pre-existing) |
| PROJ-07 | 11 | Complete (Phase 11) |
| PROJ-08 | 11 | Complete (pre-existing) |
| **Dependencies** | | |
| DEP-01 | 7 | Not started |
| DEP-02 | 7 | Not started |
| DEP-03 | 7 | Not started |
| DEP-04 | 7 | Not started |
| **Documentation** | | |
| DOC-01 | 12 | Not started |
| DOC-02 | 12 | Not started |
| DOC-03 | 12 | Not started |

**Coverage:**
- v1.1 requirements: 27 total
- Mapped to phases: 27 (complete)
- Unmapped: 0

---
*Requirements defined: 2026-03-30*
*Last updated: 2026-03-30 after research completion*
