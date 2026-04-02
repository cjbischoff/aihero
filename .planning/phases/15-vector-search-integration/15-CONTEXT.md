# Phase 15: Vector Search Integration - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Add semantic search capability using sentence-transformers embeddings (all-MiniLM-L6-v2 model) with cosine similarity. Generate embeddings for chunked documents from Day 2, cache to disk for reuse, and demonstrate vector search on course datasets handling paraphrases and conceptual queries that text search missed. This phase establishes the second of three search methods (text → vector → hybrid).

**Scope:** Vector/semantic search only. No hybrid fusion - that's Phase 16. Builds on Phase 14's text search foundation.

</domain>

<decisions>
## Implementation Decisions

### Embedding Generation Strategy
- **D-01:** Use batch processing with progress tracking (batch size: 32 chunks, configurable)
- **D-02:** Show tqdm progress bar during embedding generation (ETA, chunks/sec for user feedback)
- **D-03:** Process chunks in batches to handle large datasets gracefully (~8K chunks in 3-4 minutes)
- **D-04:** Load all-MiniLM-L6-v2 model once, reuse for all batches (model stays in memory during generation)

### Embedding Cache Management
- **D-05:** Store cache in `data/embeddings/` directory (per Phase 13 D-09, D-10, D-11)
- **D-06:** Dataset-specific cache files: `data/embeddings/datatalk_faq.npy`, `data/embeddings/evidently_docs.npy`
- **D-07:** Use numpy .npy format for cache (efficient, standard, per Phase 13 D-11)
- **D-08:** Manual cache invalidation only - user deletes cache file when chunks or model change (simple, explicit, documented in notebook)
- **D-09:** Create data/embeddings/ directory if it doesn't exist (first-time setup)
- **D-10:** Check if cache file exists before generating embeddings (load from cache if present, skip generation)

### Vector Search Interface
- **D-11:** vector_search() signature: `vector_search(query: str, top_k: int = 5) -> list[dict]` (matches text_search exactly per ORG-01)
- **D-12:** Embed query string internally on each call (simple API, <50ms overhead acceptable for course)
- **D-13:** Return format: list of dicts with score injected (same as text_search, per Phase 14 D-06, D-07, ORG-02)
- **D-14:** Score is cosine similarity float 0.0-1.0 (1.0 = identical vectors, 0.0 = orthogonal)
- **D-15:** Unified result format preserves chunk metadata (content, title, filename, chunk_id + score)

### Example Query Selection
- **D-16:** Use the 2 paraphrase queries that failed in Phase 14 text search as successes (direct comparison shows semantic search value)
- **D-17:** Phase 14 failures: "improve responses" (should match "fine-tuning"), "understanding models" (should match "machine learning")
- **D-18:** Show 1-2 vector search limitations: exact acronyms (LLM01 vs LLM02 collapse), specific codes (CVE-IDs may not match semantically)
- **D-19:** Balanced demonstration like Phase 14: successes + limitations (motivates hybrid search in Phase 16)
- **D-20:** Use same course datasets (DataTalksClub FAQ, Evidently docs) for direct comparison with Phase 14

### Integration with Day 3 Notebook
- **D-21:** Extend course/day3.ipynb (don't create new file - COURSE-09 adds to existing notebook)
- **D-22:** Add new section "Vector Search (Semantic)" after text search section
- **D-23:** Import sentence-transformers at top of new section
- **D-24:** Follow Phase 14 pattern: load data → generate/load embeddings → create index → search → analyze

### Model Download Handling
- **D-25:** Model downloads automatically to `~/.cache/huggingface/` on first SentenceTransformer() call (standard behavior)
- **D-26:** Document expected download (22MB model, happens once, cached for future runs)
- **D-27:** No need to pre-download or verify - let sentence-transformers handle it

### Claude's Discretion
- Exact batch size within 16-64 range (32 suggested, tune if needed)
- Whether to show cache hit/miss messages (informative but optional)
- Progress bar format details (chunks vs batches, custom descriptions)
- Whether to add embedding metadata (model version, timestamp) to cache (nice-to-have, not required)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Project vision, progressive enhancement pattern
- `.planning/REQUIREMENTS.md` — SEARCH-06 through SEARCH-11, COURSE-09 requirements
- `.planning/research/SUMMARY.md` — all-MiniLM-L6-v2 model details (384-dim, 14.7ms/1K tokens, CPU-optimized)

### Existing Patterns (from prior phases)
- `course/day3.ipynb` — Existing text search notebook from Phase 14 (extend with vector search section)
- `course/day1.py` — Import pattern for cross-notebook functions
- `course/day2.py` — Chunking functions (used for data prep)
- `.planning/phases/14-text-search-foundation/14-CONTEXT.md` — Text search decisions (interface to match)
- `.planning/phases/13-dependencies-setup/13-CONTEXT.md` — Embedding cache decisions (D-09, D-10, D-11)

### Data Artifacts (from prior phases)
- Day 1 output: Ingested documents (DataTalksClub FAQ, Evidently docs)
- Day 2 output: Chunked documents with `{content, title, metadata, chunk_id, filename}` schema
- Phase 13 output: sentence-transformers 5.3.0, torch 2.11.0 installed
- Phase 14 output: Text search with minsearch, paraphrase failures documented

**No external specs** — requirements fully captured in decisions above and research documentation.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Patterns
- **Notebook extension** (Phase 14): Add new section to existing day3.ipynb, don't create new file
- **Cross-notebook imports** (Phase 14): `from day1 import read_repo_data`, `from day2 import chunk_sliding_window`
- **Unified search interface** (Phase 14): `text_search(query, top_k=5) -> list[dict]` — vector_search must match
- **Result format** (Phase 14): `[{"content": ..., "title": ..., "score": ..., "chunk_id": ..., "filename": ...}]`

### Integration Points
- **Input:** Chunked documents from Day 2 (same data as Phase 14 text search)
- **Processing:** sentence-transformers.SentenceTransformer('all-MiniLM-L6-v2').encode(texts)
- **Caching:** numpy.save('data/embeddings/dataset.npy', embeddings), numpy.load() for reuse
- **Output:** vector_search() returns same format as text_search() (unified per ORG-02)

### Established Constraints
- **Python 3.13** in both course/ and project/ contexts
- **CPU-only inference** - torch 2.11.0 without CUDA (Phase 13 decision)
- **In-memory processing** - embeddings cached to disk but indices in RAM
- **Jupyter notebook** execution model - cells run sequentially, state persists

</code_context>

<specifics>
## Specific Ideas

**From research (sentence-transformers capabilities):**
- all-MiniLM-L6-v2 generates 384-dim vectors (small, fast)
- Batch encoding: `model.encode(texts, batch_size=32, show_progress_bar=True)`
- Cosine similarity: `sklearn.metrics.pairwise.cosine_similarity(query_vec, doc_vecs)`
- Model max tokens: 256 (within Day 2 chunk sizes, no truncation needed)

**Example query pairs (Phase 14 failures → Phase 15 successes):**
- **Text search fails:** "improve responses" → doesn't match "fine-tuning", "LLM optimization"
- **Vector search succeeds:** "improve responses" → matches "fine-tuning" semantically
- **Text search fails:** "understanding models" → doesn't match "machine learning", "ML basics"
- **Vector search succeeds:** "understanding models" → matches "machine learning" conceptually

**Vector search limitations to demonstrate:**
- Acronym collapse: "LLM01" and "LLM02" embed similarly (can't distinguish specific OWASP categories)
- Code specificity: CVE-2023-1234 vs CVE-2023-5678 may not distinguish semantically
- Exact terminology: "TF-IDF" as keyword is better with text search than semantic match

**Cache file structure:**
```python
# data/embeddings/datatalk_faq.npy
# Shape: (8565, 384) for ~8,565 chunks x 384-dim vectors
# Load: embeddings = np.load('data/embeddings/datatalk_faq.npy')
```

</specifics>

<deferred>
## Deferred Ideas

**Phase 16 (Hybrid Search):**
- RRF fusion combining text + vector results
- Deduplication by chunk_id across search methods
- Strategy selection framework (when to use which search type)

**Phase 17 (OWASP Application):**
- OWASP-specific queries with security terminology
- Acronym handling (LLM01-10) with hybrid search
- Domain validation on technical documentation

**Phase 18 (Polish):**
- Type hints and docstrings for all functions
- Performance metrics (embedding time, search latency)
- Learnings documentation

**Out of scope for v2.0:**
- Fine-tuned embedding models (requires labeled data)
- GPU acceleration (deferred to production)
- Vector databases (FAISS, Chroma - premature for <10K chunks)
- Query embedding caching (optimization, not learning goal)
- Embedding metadata tracking (model version, timestamp - nice-to-have)
- Automatic cache invalidation (hash-based, adds complexity)

</deferred>

---

*Phase: 15-vector-search-integration*
*Context gathered: 2026-04-02*
