# Phase 15: Vector Search Integration - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-02
**Phase:** 15-vector-search-integration
**Areas discussed:** Embedding generation strategy, cache management, vector search interface, example queries

---

## Embedding Generation Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Batch with progress (32 chunks) | Process in batches with tqdm progress bar. Shows ETA, handles large datasets. | ✓ |
| All-at-once with single progress | Pass all chunks at once, single progress indicator. Simpler but less informative. | |
| Stream processing | One chunk at a time with yield. Memory efficient but slower. | |
| No progress tracking | Silent processing. Clean but user doesn't know status. | |

**User's choice:** Batch with progress (Recommended)

**Notes:** Progress visibility is important for learning context. With ~8,565 FAQ chunks, batch processing with tqdm shows clear progress and ETA. Standard pattern for notebook workflows.

---

## Embedding Cache Naming

| Option | Description | Selected |
|--------|-------------|----------|
| Dataset-specific | data/embeddings/datatalk_faq.npy, evidently_docs.npy. Clear per-dataset separation. | ✓ |
| Hash-based | data/embeddings/<hash>.npy. Auto-invalidation but harder to inspect. | |
| Timestamp-based | data/embeddings/embeddings_2026-04-02.npy. Simple versioning but unclear content. | |
| Single cache file | data/embeddings/all_embeddings.npy with index. Efficient but complex management. | |

**User's choice:** Dataset-specific (Recommended)

**Notes:** Clear separation per dataset makes cache files easy to inspect, understand, and delete manually. Aligns with learning goals - user can see what's cached and where.

---

## Cache Invalidation Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Manual only | User deletes cache when chunks or model change. Simple, explicit, documented. | ✓ |
| Check chunk count | Compare cached count to current. Automatic but misses content changes. | |
| Hash-based detection | Hash content, compare to metadata. Accurate but adds complexity and cost. | |
| Always regenerate | Never use cache. Simple but loses 60s→<1s speedup benefit. | |

**User's choice:** Manual only (Recommended)

**Notes:** Explicit control gives user understanding of when cache is valid. Document in notebook: "Delete data/embeddings/*.npy if you change chunks or model." Avoids complexity of automatic detection while maintaining cache benefits.

---

## Vector Search Interface Consistency

| Option | Description | Selected |
|--------|-------------|----------|
| Match text_search exactly | vector_search(query, top_k=5) → list[dict]. Same signature, unified interface. | ✓ |
| Add embedding parameter | vector_search(query, top_k, embedding=None). Optional pre-computed embedding. | |
| Separate query vs embed methods | vector_search_text(), vector_search_embed(). Explicit but requires two functions. | |
| Different return format | Tuples or custom class. More structure but breaks ORG-02 unified format. | |

**User's choice:** Match exactly (Recommended)

**Notes:** Unified interface prepares for hybrid_search() in Phase 16. Same signature as text_search() makes comparison examples clearer and satisfies ORG-01 (agent integration structure).

---

## Query Embedding Handling

| Option | Description | Selected |
|--------|-------------|----------|
| Embed on each call | vector_search() embeds query internally. Simple API, <50ms overhead acceptable. | ✓ |
| Cache query embeddings | Store in-memory dict. Optimizes repeated queries but adds complexity. | |
| Require pre-embedding | User embeds before calling. Explicit but adds friction. | |
| Lazy initialization | Embed on first call, cache for session. Middle ground but adds state. | |

**User's choice:** Embed on each call (Recommended)

**Notes:** For learning phase, simplicity > optimization. <50ms embedding overhead per query is negligible. User doesn't need to think about pre-embedding. Clean, simple API.

---

## Example Query Selection

| Option | Description | Selected |
|--------|-------------|----------|
| Same failures as Phase 14 | Use 2 paraphrase queries that failed in text search. Direct before/after comparison. | ✓ |
| New conceptual queries | Different semantic queries. Broader but loses direct comparison. | |
| Mix of both | 1-2 from Phase 14 + 1-2 new. Comprehensive but may feel repetitive. | |
| User exploration | Encourage users to try their own. Interactive but less guided. | |

**User's choice:** Same failures as Phase 14 (Recommended)

**Notes:** Direct comparison is pedagogically powerful. Phase 14 showed "improve responses" failing → Phase 15 shows it succeeding via semantic matching. Clear demonstration of vector search value over text search.

---

## Balanced Examples

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, show limitations | Include 1-2 queries where vector search struggles. Motivates hybrid in Phase 16. | ✓ |
| Success-only | Show vector search at its best. Cleaner but hides trade-offs. | |
| Detailed failure analysis | Deep dive into why vectors fail. Educational but may overwhelm. | |
| Side-by-side comparison | Run same query through both. Useful but duplicates Phase 16 content. | |

**User's choice:** Yes, show limitations (Recommended)

**Notes:** Consistent with Phase 14's balanced approach (successes + failures). Show vector search excels at paraphrases but struggles with exact acronyms (LLM01 vs LLM02). This motivates why hybrid search (Phase 16) is needed - combine strengths of both.

---

## Claude's Discretion

The following areas were NOT discussed because they're implementation details:

- Exact batch size (32 suggested, tune 16-64 if needed)
- Cache hit/miss messages (informative logging, optional)
- Progress bar format (chunks vs batches, custom descriptions)
- Embedding metadata (model version, timestamp - nice-to-have)
- Cosine similarity implementation (sklearn vs manual - both work)

## Deferred Ideas

None - discussion stayed within Phase 15 scope (vector search only). Hybrid fusion and OWASP application already planned for Phases 16-17.
