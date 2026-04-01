# Roadmap: AI Hero - RAG Course

## Milestones

- **v1.0 Day 1 - GitHub Data Ingestion** -- Phases 1-6 (shipped 2026-03-30)

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

---

## v1.1 Day 2 - Document Chunking (In Progress)

**Goal:** Implement and compare multiple chunking strategies to prepare large documents for RAG systems.

**Phases:** 6 (Phases 7-12)

### Phase 7: Foundation & Dependencies
**Goal:** Establish baseline chunking with metadata preservation

**Requirements:** 8
- DEP-01: Add tiktoken to project dependencies
- DEP-02: Add openai SDK to optional dependencies
- DEP-03: Add groq SDK as alternative to OpenAI
- DEP-04: Update pyproject.toml with new dependencies
- CHUNK-01: Implement sliding window chunking (2000 chars, 1000 overlap)
- CHUNK-05: All strategies preserve metadata
- SUPPORT-01: Integrate tiktoken for accurate token counting
- SUPPORT-03: Implement metadata preservation across all chunking strategies

**Plans:** 2/2 plans complete
- [x] 07-01-PLAN.md -- Install Day 2 dependencies (tiktoken, openai, groq) in both environments
- [x] 07-02-PLAN.md -- Implement sliding window chunking and token counting in both notebooks

**Success Criteria:**
1. User can install all required dependencies (tiktoken, openai, groq) via uv
2. User can apply sliding window chunking with configurable size and overlap
3. User can verify that all Day 1 metadata (filename, frontmatter) is preserved in chunks
4. User can inspect chunk structure with `chunk_id`, `chunk_index`, `total_chunks`, `chunk_method` fields
5. User can count tokens accurately using tiktoken for target model encoding

**Status:** Complete

---

### Phase 8: Semantic Chunking
**Goal:** Structure-aware chunking respecting language and markdown boundaries

**Requirements:** 4
- CHUNK-02: Implement paragraph-based chunking using regex (`\n\s*\n` pattern)
- CHUNK-03: Implement section-based chunking by markdown headers (level 2)
- SUPPORT-02: Create strategy comparison framework (chunk counts, sizes, distribution)
- SUPPORT-04: Provide helper functions for manual inspection and analysis of chunk quality

**Plans:** 2/2 plans complete
- [x] 08-01-PLAN.md -- Implement paragraph and section chunking functions
- [x] 08-02-PLAN.md -- Implement comparison framework and quality inspection helpers

**Success Criteria:**
1. User can apply paragraph-based chunking that respects natural text boundaries
2. User can apply section-based chunking that preserves markdown header hierarchy
3. User can compare chunk counts, sizes, and distributions across all three strategies
4. User can manually inspect chunk quality to verify no code blocks or tables are split mid-content

**Status:** Complete

---

### Phase 9: LLM Chunking
**Goal:** Intelligent boundary detection with cost analysis

**Requirements:** 1
- CHUNK-04: Implement LLM-based intelligent chunking using OpenAI or Groq

**Plans:** 1 plan
- [x] 09-01-PLAN.md -- Implement LLM chunking with provider switching, cost tracking, and comparison

**Success Criteria:**
1. User can apply LLM-based semantic chunking using OpenAI or Groq API
2. User can view cost analysis showing actual API costs vs estimated costs
3. User can compare LLM chunking output against simpler strategies

**Status:** Planning complete

---

### Phase 10: Course Notebook
**Goal:** Complete Day 2 learning notebook with all strategies

**Requirements:** 6
- COURSE-01: Create new `course/day2.ipynb` notebook (follows day1.ipynb pattern)
- COURSE-02: Implement all four chunking strategies in notebook cells
- COURSE-03: Test all strategies on Evidently docs from Day 1 ingestion
- COURSE-04: Display sample outputs showing chunk structure for each strategy
- COURSE-05: Include inline explanations of token counting, overlap rationale, and semantic boundaries
- COURSE-06: Document learnings about when to use each chunking approach

**Success Criteria:**
1. User can open `course/day2.ipynb` and see all four chunking strategies implemented
2. User can run all strategies on Evidently docs from Day 1 with visible sample outputs
3. User can read inline explanations of token counting, overlap rationale, and semantic boundaries
4. User can review documented learnings about when to use each chunking approach

**Status:** Not started

---

### Phase 11: Project Homework
**Goal:** Apply chunking to OWASP docs with analysis

**Requirements:** 8
- PROJ-01: Extend existing `project/owasp_homework.ipynb` with Day 2 section
- PROJ-02: Add section header `## Day 2: Chunking` to delineate new work
- PROJ-03: Apply simple sliding window chunking to OWASP docs from Day 1
- PROJ-04: Experiment with paragraph chunking + sliding window combination
- PROJ-05: Apply section-based chunking using markdown headers
- PROJ-06: Manually inspect chunk results for each strategy
- PROJ-07: Document analysis of which chunking strategy works best for OWASP structure and why
- PROJ-08: Include engineering standards (type hints, docstrings) in chunking functions

**Success Criteria:**
1. User can open `project/owasp_homework.ipynb` and find Day 2 section after Day 1
2. User can run sliding window chunking on OWASP docs
3. User can experiment with paragraph chunking combined with sliding window
4. User can apply section-based chunking using OWASP markdown headers
5. User can review manual inspection results for each strategy
6. User can read documented analysis of which strategy works best for OWASP structure and why

**Status:** Not started

---

### Phase 12: Documentation & Synthesis
**Goal:** Document learnings and chunking tradeoffs

**Requirements:** 3
- DOC-01: Document course material learnings in `course/day2.ipynb`
- DOC-02: Document OWASP-specific findings in `project/owasp_homework.ipynb`
- DOC-03: Include code comments explaining chunking strategy tradeoffs

**Success Criteria:**
1. User can read Day 2 course material learnings documented in `course/day2.ipynb`
2. User can read OWASP-specific findings documented in `project/owasp_homework.ipynb`
3. User can find code comments explaining chunking strategy tradeoffs throughout implementation

**Status:** Not started

---

## Progress

| Phase | Milestone | Plans Complete | Status      | Completed  |
|-------|-----------|----------------|-------------|------------|
| 1-6   | v1.0      | 7/7            | Complete    | 2026-03-30 |
| 7     | v1.1      | 2/2            | Complete    | 2026-03-31 |
| 8     | v1.1      | 2/2            | Complete    | 2026-03-31 |
| 9     | v1.1      | 0/1            | Planning    | --         |
| 10-12 | v1.1      | 0/?            | Not started | --         |

---

## Next Steps

Run `/gsd:execute-phase 9` to begin Phase 9 (LLM Chunking).

---

*For historical milestones, see [MILESTONES.md](MILESTONES.md)*
