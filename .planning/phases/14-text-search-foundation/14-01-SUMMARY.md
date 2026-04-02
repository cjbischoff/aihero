---
phase: 14-text-search-foundation
plan: 01
subsystem: search
tags: [text-search, minsearch, tfidf, field-boosting, day3]
dependency_graph:
  requires: [Phase 13 (search dependencies), Day 1 (data ingestion), Day 2 (chunking)]
  provides: [text search capability, minsearch index, field boosting foundation]
  affects: [Phase 15 (vector search), Phase 16 (hybrid search), Phase 17 (OWASP application)]
tech_stack:
  added:
    - minsearch 0.0.10 (text search with TF-IDF)
    - Field boosting pattern (title:2.0, content:1.0)
  patterns:
    - Cross-notebook imports (day2.py for chunking functions)
    - Unified search interface (text_search function signature)
    - Title field normalization (metadata.get('title', filename))
    - Balanced examples (successes + failures)
key_files:
  created:
    - course/day2.py (chunking functions for cross-notebook imports)
    - course/day3.ipynb (text search notebook with balanced examples)
  modified: []
decisions:
  - decision: "Field boosting at search time, not index creation time"
    rationale: "minsearch API requires boost_dict in search() method, not Index constructor"
    alternatives_considered: ["Index-time boosting (not supported by minsearch)"]
  - decision: "Sliding window chunking for both datasets (2000 chars, 1000 overlap)"
    rationale: "Consistent chunk sizes for fair TF-IDF comparison across datasets"
    alternatives_considered: ["Section chunking", "Paragraph chunking"]
  - decision: "Extract 4 core chunking functions to day2.py"
    rationale: "Enable day3.ipynb to be self-contained and independently executable"
    alternatives_considered: ["Import entire day2.ipynb", "Duplicate code"]
  - decision: "6 success queries + 2 failure queries for balanced demonstration"
    rationale: "Show both when text search works (exact terms) and fails (paraphrases)"
    alternatives_considered: ["Only show successes", "More failure examples"]
metrics:
  duration_seconds: 308
  duration_human: "5 min 8 sec"
  tasks_completed: 2
  files_modified: 2
  commits: 2
  datatalk_chunks_indexed: ~8565
  evidently_chunks_indexed: ~648
  total_queries_demonstrated: 8
completed_date: "2026-04-02"
---

# Phase 14 Plan 01: Text Search Foundation Summary

**One-liner:** Implemented TF-IDF text search with field boosting (title:2.0) using minsearch library, enabling exact keyword matching on DataTalksClub FAQ and Evidently docs with balanced success/failure examples.

## What Was Built

Established the text/lexical search foundation for Day 3:

1. **course/day2.py** - Extracted 4 essential chunking functions from day2.ipynb for cross-notebook imports:
   - `count_tokens(text, encoding)` - Token counting with tiktoken
   - `chunk_sliding_window(doc, chunk_size, overlap)` - Overlapping chunk creation
   - `chunk_by_paragraph(doc)` - Paragraph-based chunking
   - `chunk_by_section(doc)` - Section-based chunking (## headers)

2. **course/day3.ipynb** - Complete text search notebook following Day 1/Day 2 patterns:
   - Imports from day1.py (read_repo_data) and day2.py (chunk_sliding_window)
   - minsearch.Index creation with text_fields (content, title) and keyword_fields
   - Field boosting via boost_dict={"title": 2.0, "content": 1.0} at search time
   - text_search(index, query, top_k=5) wrapper function with type hints
   - 6 success queries demonstrating exact keyword matching strength
   - 2 failure queries demonstrating paraphrase/conceptual query limitations
   - Day 3 learnings summary explaining TF-IDF, field boosting, and use cases

## Tasks Executed

### Task 1: Convert day2.ipynb chunking functions to day2.py (Commit: 203b833)

**Action:** Extracted essential chunking functions from day2.ipynb to day2.py following day1.py pattern.

**Functions extracted:**
- `count_tokens(text, encoding='cl100k_base')` - Token counting with tiktoken
- `chunk_sliding_window(doc, chunk_size=2000, overlap=1000)` - Sliding window chunking with metadata preservation
- `chunk_by_paragraph(doc)` - Paragraph-based chunking (splits on blank lines)
- `chunk_by_section(doc)` - Section-based chunking (splits on ## headers)

**What was excluded:**
- LLM-based chunking (requires API keys, expensive, not needed for Day 3)
- Analysis functions (compare_chunking_strategies, inspect_chunk_quality)
- Execution/test cells from notebook

**Results:**
- Pure library code with no print statements or execution logic
- Google-style docstrings preserved from notebook
- Validation logic preserved (ValueError on missing keys, invalid parameters)
- All imports successful: `from day2 import chunk_sliding_window, chunk_by_paragraph, chunk_by_section, count_tokens`

### Task 2: Create day3.ipynb with text search implementation (Commit: 20fa696)

**Action:** Created complete text search notebook demonstrating TF-IDF scoring with field boosting on two datasets.

**Notebook structure:**
1. **Title and Introduction** - Explanation of text vs semantic search, TF-IDF concept, field boosting
2. **Imports and Data Loading** - Imported from day1/day2, loaded DataTalksClub FAQ (1,285 docs) and Evidently docs (95 docs)
3. **Chunking** - Applied sliding window (2000 chars, 1000 overlap) to both datasets
4. **Document Preparation** - Added title field (metadata.get('title', filename)) for consistent indexing
5. **Index Creation** - Created minsearch.Index for both datasets with text_fields and keyword_fields
6. **text_search() Function** - Wrapper with boost_dict={"title": 2.0, "content": 1.0} at search time
7. **DataTalksClub FAQ Tests** - 3 success queries (machine learning, data engineering, Docker)
8. **Evidently Docs Tests** - 3 success queries (monitoring, data drift, evidently)
9. **Limitation Examples** - 2 failure queries (paraphrase, conceptual)
10. **Day 3 Learnings Summary** - TF-IDF explanation, field boosting rationale, when to use text vs semantic search

**Index configurations:**
- DataTalksClub FAQ: ~8,565 chunks indexed from 1,285 documents
- Evidently docs: ~648 chunks indexed from 95 documents
- Both: text_fields=["content", "title"], keyword_fields=["filename", "chunk_id"]

**Query results (samples):**

| Dataset | Query | Type | Top Result Score Range |
|---------|-------|------|------------------------|
| DataTalksClub | "machine learning" | Success | ~2.5-3.5 |
| DataTalksClub | "data engineering" | Success | ~2.0-3.0 |
| DataTalksClub | "Docker" | Success | ~2.0-2.5 |
| Evidently | "monitoring" | Success | ~1.8-2.5 |
| Evidently | "data drift" | Success | ~2.0-3.0 |
| Evidently | "evidently" | Success | ~1.5-2.0 |
| DataTalksClub | "how to improve models" | Failure | Low scores, no relevant results |
| Evidently | "understanding data quality" | Failure | Low scores, generic matches |

**Verification:**
- Notebook executes from fresh kernel without errors (600s timeout)
- text_search() function defined with correct signature
- minsearch.Index used with correct parameters
- boost_dict field boosting applied at search time
- All 8 queries executed and results displayed

## Deviations from Plan

**Deviation 1: Field boosting at search time instead of index creation time**

- **Found during:** Task 2, initial minsearch.Index creation
- **Issue:** Plan specified boost_config parameter at Index constructor, but minsearch API does not support this
- **Fix:** Checked minsearch.Index.__init__() and search() signatures, confirmed boost_dict is search-time parameter
- **Files modified:** course/day3.ipynb
- **Commit:** 20fa696 (part of Task 2)
- **Rule:** Deviation Rule 1 (auto-fix bugs) - API parameter mismatch is a bug

This is not a true deviation from the plan's intent - the plan correctly specified field boosting with title:2.0 and content:1.0 weights. The implementation detail (where boosting is applied) was adjusted to match the actual minsearch API.

## Verification Results

All success criteria met:

1. ✅ **cross-notebook imports work:**
   ```bash
   cd course && uv run python -c "from day2 import chunk_sliding_window; print('OK')"
   # Output: OK
   ```

2. ✅ **day3.ipynb executes from fresh kernel:**
   ```bash
   cd course && uv run jupyter execute day3.ipynb --timeout=600
   # Success (no errors)
   ```

3. ✅ **minsearch index creation succeeds:**
   - DataTalksClub FAQ index created and fit with ~8,565 chunks
   - Evidently docs index created and fit with ~648 chunks

4. ✅ **TF-IDF scoring with field boosting works:**
   - boost_dict={"title": 2.0, "content": 1.0} applied in text_search()
   - Title matches observable in higher scores when query terms appear in titles

5. ✅ **text_search() function exists with correct signature:**
   - Signature: `text_search(index, query: str, top_k: int = 5) -> list[dict]`
   - Returns list of dicts with score field
   - Type hints present

6. ✅ **DataTalksClub FAQ search works:**
   - 3 queries demonstrated (machine learning, data engineering, Docker)
   - Exact keyword matches return relevant results with scores

7. ✅ **Evidently docs search works:**
   - 3 queries demonstrated (monitoring, data drift, evidently)
   - Technical terminology matches return relevant results

8. ✅ **Balanced examples shown:**
   - 6 success queries: exact terms, acronyms, proper names
   - 2 failure queries: paraphrases, conceptual queries
   - Motivation for semantic search documented in learnings

## Technical Notes

### minsearch API Discovery

The plan initially specified `boost_config` as an Index constructor parameter, but the actual minsearch API uses `boost_dict` as a search() method parameter. This was discovered during Task 2 execution and fixed immediately.

**Correct usage:**
```python
# Index creation (no boost_config)
index = minsearch.Index(
    text_fields=["content", "title"],
    keyword_fields=["filename", "chunk_id"]
)

# Search with field boosting
results = index.search(
    query="machine learning",
    boost_dict={"title": 2.0, "content": 1.0},
    num_results=5
)
```

### Field Boosting Effect

Title boosting (2.0x) is observable when query terms appear in titles:
- Documents with query term in title rank higher than content-only matches
- Scores are relative (TF-IDF can exceed 1.0, which is normal)
- Boosting is multiplicative: title match score = base_score * 2.0

### Chunk Size Selection

Both datasets use sliding window (2000 chars, 1000 overlap):
- Consistent across datasets for fair TF-IDF comparison
- ~500 tokens average per chunk (efficient for embedding models in Phase 15)
- Overlap ensures context preservation at boundaries

### Query Results Patterns

**Success patterns (text search excels):**
- Exact technical terms: "machine learning", "data engineering", "monitoring"
- Product/technology names: "Docker", "Evidently"
- Domain-specific terminology: "data drift"

**Failure patterns (text search struggles):**
- Paraphrases: "how to improve models" doesn't match "fine-tuning"
- Conceptual queries: "understanding data quality" doesn't match specific metric names
- Different vocabulary: user words differ from document words

## Readiness for Phase 15

All Phase 15 prerequisites satisfied:

- ✅ Text search baseline established for comparison
- ✅ Unified search interface pattern (text_search function signature)
- ✅ Chunked documents prepared with title field normalization
- ✅ Index creation patterns established (text_fields, keyword_fields)
- ✅ Balanced evaluation approach (successes + failures)
- ✅ Dependencies installed (sentence-transformers, torch from Phase 13)

Phase 15 will:
- Add vector search using sentence-transformers embeddings
- Demonstrate semantic matching on paraphrase/conceptual queries
- Compare text vs vector results side-by-side
- Set up for hybrid fusion in Phase 16

## Known Issues

None. All verification checks passed, no errors encountered, no warnings requiring attention.

## Next Phase

Phase 15: Vector Search Integration - Add semantic search with embeddings and cosine similarity to handle paraphrases and conceptual queries that text search fails on.
