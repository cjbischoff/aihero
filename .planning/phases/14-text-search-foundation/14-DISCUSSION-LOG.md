# Phase 14: Text Search Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-02
**Phase:** 14-text-search-foundation
**Areas discussed:** Field boosting, search function interface, example query selection

---

## Field Boosting Configuration

| Option | Description | Selected |
|--------|-------------|----------|
| Moderate (title:2.0, content:1.0) | Clear preference for title matches, easy to observe. Common production pattern. | ✓ |
| Strong (title:3.0, description:2.0) | Title matches dominate. Good for structured docs, may miss content-only matches. | |
| Subtle (title:1.5, content:1.0) | Gentle preference. Harder to observe effect in examples. | |
| No boosting (flat weights) | Pure TF-IDF, no field preferences. Simplest but misses structural info. | |

**User's choice:** Moderate (title:2.0, content:1.0) - Recommended

**Notes:** Balances observable ranking effects with recall. Title matches get 2x weight - enough to see in examples, not so much that content-only matches disappear. Aligns with production patterns from research.

---

## Search Function Interface - Parameters

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal (query, top_k) | Just query string and result count. Boosting pre-configured. Simple API. | ✓ |
| Extended (query, top_k, boost_fields, filter) | Runtime boosting/filtering control. More flexible but complex. | |
| Query-only (query, top_k=5 default) | Simplest possible. Fixed default, very beginner-friendly. | |
| Full control (query, top_k, min_score, boost_dict, filter_dict) | Maximum configurability. Good for production, overkill for learning. | |

**User's choice:** Minimal (query, top_k) - Recommended

**Notes:** Clean API with just query and top_k. Boosting configured at index creation (implementation detail, not user-facing parameter). Prepares for unified interface with vector_search and hybrid_search (ORG-01 requirement).

---

## Search Function Interface - Return Format

| Option | Description | Selected |
|--------|-------------|----------|
| Dict with score+metadata | Returns [{content, title, score, chunk_id, ...}]. Full context, ready for display/LLM. | ✓ |
| Tuple (score, chunk_dict) | Returns [(0.85, {chunk_dict})]. Separates score from document. | |
| Chunk dict with injected score | Adds 'score' key to chunk dicts. Simple but mutates originals. | |
| Custom SearchResult class | Dedicated type with .score, .content, .metadata. More structure but requires class def. | |

**User's choice:** Dict with score+metadata - Recommended

**Notes:** List of dicts with score field added to chunk schema. Consistent with Day 1/Day 2 patterns (everything is dicts). Easy to inspect in notebooks, easy to serialize, easy to pass to LLMs. Satisfies ORG-02 (unified result format).

---

## Example Query Selection - Query Type

| Option | Description | Selected |
|--------|-------------|----------|
| Balanced (successes + failures) | Show 2-3 where text search excels, 1-2 where it struggles. Motivates hybrid. | ✓ |
| Success-focused (only good matches) | Show text search at its best. Save limitations for vector phase. | |
| Limitation-focused (emphasize failures) | More time on what text search misses. Strong motivation but feels negative. | |
| Exploratory (user tries their own) | Provide 1 example, encourage experimentation. Interactive but less guided. | |

**User's choice:** Balanced (successes + failures) - Recommended

**Notes:** Show text search strengths (exact terms, acronyms, titles) AND limitations (paraphrases, conceptual queries). This naturally motivates why semantic search (Phase 15) and hybrid search (Phase 16) are needed. Tells complete story per phase rather than painting text search as perfect.

---

## Example Query Selection - Dataset Focus

| Option | Description | Selected |
|--------|-------------|----------|
| Course datasets only | DataTalksClub FAQ and Evidently docs per SEARCH-04/SEARCH-05. Save OWASP for Phase 17. | ✓ |
| Course + preview OWASP | Show course examples, add 1 OWASP query as teaser. Builds continuity. | |
| OWASP-heavy | Focus on OWASP corpus. But contradicts roadmap (OWASP is Phase 17). | |
| Let user choose dataset interactively | Parameterize examples. Flexible but adds complexity. | |

**User's choice:** Course datasets only - Recommended

**Notes:** Strict adherence to roadmap phase boundaries. Phase 14 uses course datasets (FAQ, Evidently), Phase 17 applies to OWASP. Clear separation avoids scope creep and matches requirements SEARCH-04 (FAQ) and SEARCH-05 (Evidently). OWASP homework comes later with full context from Phases 14-16.

---

## Claude's Discretion

The following areas were NOT discussed because they're implementation details:

- Exact queries to demonstrate (within "balanced" framework) - planner chooses specific queries
- Whether to show minsearch.Index internals or treat as black box - depends on pedagogical flow
- Order of notebook sections - follows Day 1/Day 2 patterns (intro → code → demo → reflect)
- Whether to include timing metrics - nice-to-have, not critical for Phase 14
- Top-K default value - suggested 5, can adjust if datasets are very small/large

## Deferred Ideas

None - discussion stayed within Phase 14 scope (text search only). Vector search and hybrid fusion already planned for Phases 15-16.
