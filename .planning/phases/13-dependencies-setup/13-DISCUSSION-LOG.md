# Phase 13: Dependencies & Setup - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-01
**Phase:** 13-dependencies-setup
**Areas discussed:** Embedding cache strategy

---

## Embedding Cache Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| data/embeddings/ | Visible data directory - easy to inspect, clear, delete. Standard for course learning. | ✓ |
| .cache/embeddings/ | Hidden cache directory - follows Unix/Python conventions, auto-managed. | |
| Per-context (course/.cache, project/.cache) | Isolated caches per folder - avoids model version conflicts. | |

**User's choice:** data/embeddings/ (Recommended)

**Notes:** Selected for visibility and ease of inspection - fits course learning context where users should understand what's being cached and where. Aligns with v1.0-v1.1 pattern of keeping data artifacts visible rather than hidden.

---

## Claude's Discretion

- Exact torch version within >=2.0.0 range (use current stable)
- Order of dependency installation (optimize for efficiency)
- Whether to verify model download in this phase or defer to Phase 15

## Deferred Ideas

None - phase scope is dependency installation only, no search implementation.
