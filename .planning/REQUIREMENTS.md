# Requirements: v2.0 Day 3 - Add Search

**Milestone Goal:** Build a working search system combining lexical and semantic approaches to enable efficient information retrieval from prepared documents.

**Defined:** 2026-04-01
**Core Value:** Implement text/lexical, vector/semantic, and hybrid search to demonstrate how modern RAG systems find relevant information.

---

## v2.0 Requirements

### Dependencies

- [x] **DEP-04**: Add minsearch library to project dependencies (course-specified for text + vector search)
- [x] **DEP-05**: Add sentence-transformers library with all-MiniLM-L6-v2 model (384-dim embeddings)
- [x] **DEP-06**: Add torch as PyTorch backend for sentence-transformers (CPU-only sufficient)
- [x] **DEP-07**: Update pyproject.toml and regenerate requirements.lock with new dependencies

### Text Search (Lexical)

- [x] **SEARCH-01**: Create minsearch.Index for text/lexical search on chunked documents
- [x] **SEARCH-02**: Index text fields (chunk content, title, description, filename) with TF-IDF scoring
- [x] **SEARCH-03**: Implement text_search() function with relevance scoring and configurable top-K retrieval
- [x] **SEARCH-04**: Test text search on DataTalksClub FAQ (data engineering subset) with sample queries
- [x] **SEARCH-05**: Test text search on Evidently docs from Day 1 with sample queries

### Vector Search (Semantic)

- [x] **SEARCH-06**: Load sentence-transformers with all-MiniLM-L6-v2 model (384-dim embeddings, CPU-optimized)
- [x] **SEARCH-07**: Generate embeddings for chunked documents with progress tracking (tqdm for visibility)
- [x] **SEARCH-08**: Cache embeddings to disk as numpy arrays (.npy format) to avoid recomputation (1-2 min → <1 sec)
- [x] **SEARCH-09**: Create minsearch.VectorSearch index with pre-computed embeddings
- [x] **SEARCH-10**: Implement vector_search() function with cosine similarity and configurable top-K retrieval
- [x] **SEARCH-11**: Test vector search on same course datasets (FAQ + Evidently) with semantic queries

### Hybrid Search

- [x] **SEARCH-12**: Implement hybrid_search() function combining text and vector results with deduplication
- [x] **SEARCH-13**: Use Reciprocal Rank Fusion (RRF) with k=60 for parameter-free score combination
- [x] **SEARCH-14**: Implement deduplication by chunk_id or filename to avoid duplicate results
- [x] **SEARCH-15**: Compare all three approaches (text vs vector vs hybrid) with side-by-side examples

### Code Organization

- [x] **ORG-01**: Structure search functions for agent integration (text_search, vector_search, hybrid_search with consistent signatures)
- [x] **ORG-02**: Establish unified result format with metadata (filename, title, content, score, chunk_id)
- [x] **ORG-03**: Ensure reproducible execution from fresh kernel (import Day 1/Day 2 functions as needed)
- [x] **ORG-04**: Document search strategy selection (exact keywords → text, concepts → vector, best results → hybrid)

### Course Implementation (course/)

- [x] **COURSE-07**: Create course/day3.ipynb following established course notebook pattern
- [x] **COURSE-08**: Implement text search on DataTalksClub FAQ with example queries demonstrating exact matching
- [x] **COURSE-09**: Implement vector search on Evidently docs with semantic queries showing conceptual matching
- [x] **COURSE-10**: Implement hybrid search combining both approaches with RRF fusion
- [x] **COURSE-11**: Include comparison examples showing when each approach works best (e.g., acronyms vs paraphrases)
- [x] **COURSE-12**: Document search strategy selection decision framework with tradeoffs table

### OWASP Homework (project/)

- [x] **HOMEWORK-01**: Extend project/owasp_homework.ipynb with Day 3 section following Day 1/Day 2 pattern
- [x] **HOMEWORK-02**: Add section header `## Day 3: Search` to clearly delineate new work
- [x] **HOMEWORK-03**: Index OWASP chunked documents (from Day 2) with text search (minsearch.Index)
- [x] **HOMEWORK-04**: Generate and cache embeddings for OWASP docs with vector search (sentence-transformers)
- [x] **HOMEWORK-05**: Implement hybrid search on OWASP corpus with RRF fusion (k=60)
- [x] **HOMEWORK-06**: Experiment with all three approaches on OWASP-specific queries (security terminology)
- [x] **HOMEWORK-07**: Test acronym handling (LLM01-10, CVE-IDs) across all search methods to understand limitations
- [x] **HOMEWORK-08**: Manually inspect search results for each strategy (relevance, precision, recall intuition)
- [x] **HOMEWORK-09**: Document analysis: which approach works best for security documentation structure and why
- [x] **HOMEWORK-10**: Address technical terminology challenges (acronyms, codes, precise terms vs conceptual queries)
- [x] **HOMEWORK-11**: Apply engineering standards (type hints, docstrings per PROJ-08 pattern) to search functions

---

## Traceability

Requirements mapped to roadmap phases:

| Requirement | Phase | Status |
|-------------|-------|--------|
| DEP-04 | Phase 13 | Complete |
| DEP-05 | Phase 13 | Complete |
| DEP-06 | Phase 13 | Complete |
| DEP-07 | Phase 13 | Complete |
| SEARCH-01 | Phase 14 | Complete |
| SEARCH-02 | Phase 14 | Complete |
| SEARCH-03 | Phase 14 | Complete |
| SEARCH-04 | Phase 14 | Complete |
| SEARCH-05 | Phase 14 | Complete |
| ORG-01 | Phase 14 | Complete |
| ORG-02 | Phase 14 | Complete |
| ORG-03 | Phase 14 | Complete |
| COURSE-07 | Phase 14 | Complete |
| COURSE-08 | Phase 14 | Complete |
| SEARCH-06 | Phase 15 | Complete |
| SEARCH-07 | Phase 15 | Complete |
| SEARCH-08 | Phase 15 | Complete |
| SEARCH-09 | Phase 15 | Complete |
| SEARCH-10 | Phase 15 | Complete |
| SEARCH-11 | Phase 15 | Complete |
| COURSE-09 | Phase 15 | Complete |
| SEARCH-12 | Phase 16 | Complete |
| SEARCH-13 | Phase 16 | Complete |
| SEARCH-14 | Phase 16 | Complete |
| SEARCH-15 | Phase 16 | Complete |
| ORG-04 | Phase 16 | Complete |
| COURSE-10 | Phase 16 | Complete |
| COURSE-11 | Phase 16 | Complete |
| COURSE-12 | Phase 16 | Complete |
| HOMEWORK-01 | Phase 17 | Complete |
| HOMEWORK-02 | Phase 17 | Complete |
| HOMEWORK-03 | Phase 17 | Complete |
| HOMEWORK-04 | Phase 17 | Complete |
| HOMEWORK-05 | Phase 17 | Complete |
| HOMEWORK-06 | Phase 17 | Complete |
| HOMEWORK-07 | Phase 17 | Complete |
| HOMEWORK-08 | Phase 17 | Complete |
| HOMEWORK-09 | Phase 17 | Complete |
| HOMEWORK-10 | Phase 17 | Complete |
| HOMEWORK-11 | Phase 17 | Complete |

**Coverage:** 42/42 requirements mapped (100%)

---

## Future Requirements (Deferred to Day 4-7)

### Advanced Search Features
- **RERANK-01**: Cross-encoder reranking for +30-50% accuracy improvement (adds 120ms latency)
- **FUSION-02**: Query-aware adaptive fusion (different weights by query type, requires classification)
- **EMBED-02**: Fine-tuned embedding models for domain-specific terminology (requires labeled data)

### Scale & Performance
- **SCALE-01**: Vector databases (Chroma, FAISS, Qdrant) for >10K chunk corpora
- **SCALE-02**: Real-time indexing for dynamic document collections
- **PERF-01**: GPU acceleration for embedding generation at scale

### Agent Integration
- **AGENT-01**: Conversational interface with search integration (Day 4-7)
- **AGENT-02**: Multi-turn query refinement based on search results
- **AGENT-03**: Context-aware result presentation and summarization

---

## Out of Scope (Explicitly Excluded from v2.0)

### Premature Optimizations
| Feature | Reason |
|---------|--------|
| **OpenAI Embeddings API** | Use local sentence-transformers (free, no rate limits, course requirement, offline-capable) |
| **Multiple vector databases** | 542 OWASP docs (~2K chunks) fit in memory; infrastructure premature for learning goals |
| **BM25 instead of TF-IDF** | minsearch uses TF-IDF (acceptable for course); BM25 is production upgrade path (documented) |
| **GPU acceleration** | CPU inference sufficient for course scale (14.7ms/1K tokens all-MiniLM-L6-v2) |
| **Cross-encoder reranking** | Day 4+ feature (two-stage retrieval adds complexity beyond fundamentals) |

### Anti-Patterns
| Feature | Reason |
|---------|--------|
| **Auto-query rewriting with LLM** | Adds latency, cost, unpredictability; can make queries worse; hard to debug (research-flagged anti-feature) |
| **Only embeddings without lexical** | Fails on exact terminology, acronyms (LLM01), CVE-IDs; hybrid compensates for embedding weaknesses |
| **Linear combination score fusion** | BM25 (0-100+) vs cosine (0-1) causes "tidal wave" effect; use RRF instead (parameter-free, production-validated) |
| **Fine-tuned models without validation** | Requires 100s-1000s labeled pairs, marginal gains, expensive to maintain (defer to advanced milestones) |

### Complexity Beyond Course Scope
- **Real-time indexing**: Static corpus sufficient for course (batch indexing pattern matches Day 1/Day 2)
- **Field-level boosting tuning**: Start with minsearch defaults (title: 2.0, content: 1.0), tune only if needed
- **Custom tokenization**: Use minsearch defaults; shared tokenizer function prevents index/query mismatches
- **Quantized models**: Production optimization (ONNX, int8); course focuses on fundamentals first

**Rationale:** Day 3 focuses on fundamental search concepts. Production optimizations, infrastructure, and advanced features defer to Day 4-7 milestones per PROJECT.md evolution plan.

---

*Last updated: 2026-04-01 | v2.0 requirements defined based on Day 3 course materials + ecosystem research*
