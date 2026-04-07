# Roadmap: AI Hero - RAG Course

## Milestones

- ✅ **v1.0 Day 1 - GitHub Data Ingestion** — Phases 1-6 (shipped 2026-03-30)
- ✅ **v1.1 Day 2 - Document Chunking** — Phases 7-12 (shipped 2026-04-01)
- ✅ **v2.0 Day 3 - Add Search** — Phases 13-18 (shipped 2026-04-06)
- 🚧 **v4.0 Day 4 - Agents and Tools** — Phases 19-24 (in progress)

## Phases

<details>
<summary>✅ v1.0 Day 1 - GitHub Data Ingestion (Phases 1-6) — SHIPPED 2026-03-30</summary>

- [x] Phase 1: Environment Setup (1/1 plans) — completed 2026-03-30
- [x] Phase 2: Course Project Initialization (1/1 plans) — completed 2026-03-30
- [x] Phase 3: Core Implementation (1/1 plans) — completed 2026-03-30
- [x] Phase 4: Course Validation (2/2 plans) — completed 2026-03-30
- [x] Phase 5: Project Homework (1/1 plans) — completed 2026-03-30
- [x] Phase 6: Documentation & Reflection (1/1 plans) — completed 2026-03-30

**Total:** 7 plans completed

See [v1.0 milestone archive](milestones/1.0-ROADMAP.md) for full details.

</details>

<details>
<summary>✅ v1.1 Day 2 - Document Chunking (Phases 7-12) — SHIPPED 2026-04-01</summary>

- [x] Phase 7: Foundation & Dependencies (2/2 plans) — completed 2026-03-31
- [x] Phase 8: Semantic Chunking (2/2 plans) — completed 2026-03-31
- [x] Phase 9: LLM Chunking (1/1 plans) — completed 2026-04-01
- [x] Phase 10: Course Notebook (1/1 plans) — completed 2026-04-01
- [x] Phase 11: Project Homework (1/1 plans) — completed 2026-04-01
- [x] Phase 12: Documentation & Synthesis (1/1 plans) — completed 2026-04-01

**Total:** 8 plans completed

See [v1.1 milestone archive](milestones/1.1-ROADMAP.md) for full details.

</details>

<details>
<summary>✅ v2.0 Day 3 - Add Search (Phases 13-18) — SHIPPED 2026-04-06</summary>

- [x] Phase 13: Dependencies & Setup (1/1 plans) — completed 2026-04-02
- [x] Phase 14: Text Search Foundation (1/1 plans) — completed 2026-04-02
- [x] Phase 15: Vector Search Integration (1/1 plans) — completed 2026-04-03
- [x] Phase 16: Hybrid Search via RRF (1/1 plans) — completed 2026-04-03
- [x] Phase 17: OWASP Application & Analysis (3/3 plans) — completed 2026-04-05
- [x] Phase 18: Documentation & Code Quality (1/1 plans) — completed 2026-04-06

**Total:** 8 plans completed

See [v2.0 milestone archive](milestones/v2.0-ROADMAP.md) for full details.

</details>

---

### 🚧 v4.0 Day 4 - Agents and Tools (In Progress)

**Milestone Goal:** Build AI agents that can use search tools to answer questions based on indexed documentation

**Overview:** v4.0 builds the agent layer on top of existing search infrastructure (Days 1-3). Starting with dependency setup and search function preparation, we'll implement agents using both manual OpenAI API (educational) and Pydantic AI framework (production pattern). The course deliverable demonstrates FAQ question-answering, while the OWASP implementation applies agent patterns to security documentation with domain-specific tuning.

#### Phase 19: Dependency Setup & Search Preparation
**Goal**: Agent infrastructure ready with search tools prepared for tool calling
**Depends on**: Nothing (first phase, builds on v2.0 search functions)
**Requirements**: PYDANTIC-01, AGENT-06
**Success Criteria** (what must be TRUE):
  1. pydantic-ai dependency installed in both course/ and project/ pyproject.toml
  2. Search functions (text_search, vector_search, hybrid_search) have type hints and docstrings
  3. Dependencies verified working via import test in both contexts
**Plans**: 1 plan

Plans:
- [x] 19-01-PLAN.md — Install pydantic-ai and add type hints to search functions

#### Phase 20: Manual OpenAI Agent
**Goal**: Working agent using raw OpenAI API demonstrating function calling fundamentals
**Depends on**: Phase 19
**Requirements**: AGENT-01, AGENT-02, AGENT-03, AGENT-04, AGENT-05, AGENT-07, AGENT-08, COURSE-02
**Success Criteria** (what must be TRUE):
  1. Agent can receive user question and invoke text_search tool based on LLM decision
  2. Tool results flow back to LLM for final response generation
  3. Conversation history managed correctly across multiple turns (stateless LLM pattern)
  4. Error handling prevents crashes when search returns empty results
  5. Loop termination prevents infinite tool calls (20-step limit)
**Plans**: 1 plan

Plans:
- [x] 20-01-PLAN.md — Implement manual OpenAI agent with function calling fundamentals

#### Phase 21: Pydantic AI Framework Migration
**Goal**: Same agent behavior with cleaner, production-ready code
**Depends on**: Phase 20
**Requirements**: PYDANTIC-02, PYDANTIC-03, PYDANTIC-04, PYDANTIC-05, COURSE-03
**Success Criteria** (what must be TRUE):
  1. Pydantic AI agent produces same results as manual OpenAI version
  2. Tool schema auto-generated from type hints and docstrings (no manual JSON)
  3. Agent reasoning breakdown visible via result.new_messages()
  4. Code complexity reduced compared to manual version (fewer lines, clearer intent)
**Plans**: 1 plan

Plans:
- [ ] 21-01-PLAN.md — Extend day4.ipynb with Pydantic AI framework section

#### Phase 22: Course Deliverable
**Goal**: course/day4.ipynb reproduces Day 4 materials with FAQ agent
**Depends on**: Phase 21
**Requirements**: COURSE-01, COURSE-04, COURSE-05, COURSE-06, COURSE-07
**Success Criteria** (what must be TRUE):
  1. FAQ agent answers questions using DataTalksClub corpus from Day 3
  2. Both manual OpenAI and Pydantic AI versions demonstrated side-by-side
  3. System prompt experiments show measurable behavior variation (2-3 variants tested)
  4. Learnings documented in markdown cells (agentic behavior, stateless pattern, tool use)
  5. Notebook runs top-to-bottom from fresh kernel without errors
**Plans**: TBD
**UI hint**: yes

Plans:
- [ ] TBD

#### Phase 23: OWASP Security Agent
**Goal**: Agent applied to OWASP corpus with security domain-specific tuning
**Depends on**: Phase 22
**Requirements**: HOMEWORK-01, HOMEWORK-02, HOMEWORK-03, HOMEWORK-04, HOMEWORK-05, HOMEWORK-06
**Success Criteria** (what must be TRUE):
  1. OWASP agent uses hybrid_search tool (optimal from v2.0 research)
  2. System prompt tuned for security terminology and OWASP context
  3. 5+ OWASP-specific queries tested (LLM01-10 lookups, CVE references, security concepts)
  4. Engineering standards applied (type hints, docstrings, inline comments explaining tradeoffs)
  5. Day 4 section added to project/owasp_homework.ipynb with clear header
**Plans**: TBD
**UI hint**: yes

Plans:
- [ ] TBD

#### Phase 24: Documentation & Final Verification
**Goal**: All documentation updated, reproducibility verified, milestone complete
**Depends on**: Phase 23
**Requirements**: ORG-01, ORG-02, ORG-03, ORG-04, ORG-05
**Success Criteria** (what must be TRUE):
  1. All 3 README.md files (course/, project/, root) reflect v4.0 status and Day 4 content
  2. Architecture diagram created in docs/diagrams/agent-tool-architecture.md
  3. Both course/day4.ipynb and project/owasp_homework.ipynb run top-to-bottom from fresh kernel
  4. No hardcoded paths, credentials, or absolute file references in committed code
**Plans**: TBD

Plans:
- [ ] TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 19 → 20 → 21 → 22 → 23 → 24

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Environment Setup | v1.0 | 1/1 | Complete | 2026-03-30 |
| 2. Course Project Initialization | v1.0 | 1/1 | Complete | 2026-03-30 |
| 3. Core Implementation | v1.0 | 1/1 | Complete | 2026-03-30 |
| 4. Course Validation | v1.0 | 2/2 | Complete | 2026-03-30 |
| 5. Project Homework | v1.0 | 1/1 | Complete | 2026-03-30 |
| 6. Documentation & Reflection | v1.0 | 1/1 | Complete | 2026-03-30 |
| 7. Foundation & Dependencies | v1.1 | 2/2 | Complete | 2026-03-31 |
| 8. Semantic Chunking | v1.1 | 2/2 | Complete | 2026-03-31 |
| 9. LLM Chunking | v1.1 | 1/1 | Complete | 2026-04-01 |
| 10. Course Notebook | v1.1 | 1/1 | Complete | 2026-04-01 |
| 11. Project Homework | v1.1 | 1/1 | Complete | 2026-04-01 |
| 12. Documentation & Synthesis | v1.1 | 1/1 | Complete | 2026-04-01 |
| 13. Dependencies & Setup | v2.0 | 1/1 | Complete | 2026-04-02 |
| 14. Text Search Foundation | v2.0 | 1/1 | Complete | 2026-04-02 |
| 15. Vector Search Integration | v2.0 | 1/1 | Complete | 2026-04-03 |
| 16. Hybrid Search via RRF | v2.0 | 1/1 | Complete | 2026-04-03 |
| 17. OWASP Application & Analysis | v2.0 | 3/3 | Complete | 2026-04-05 |
| 18. Documentation & Code Quality | v2.0 | 1/1 | Complete | 2026-04-06 |
| 19. Dependency Setup & Search Preparation | v4.0 | 1/1 | Complete   | 2026-04-07 |
| 20. Manual OpenAI Agent | v4.0 | 1/1 | Complete   | 2026-04-07 |
| 21. Pydantic AI Framework Migration | v4.0 | 0/1 | Planned | - |
| 22. Course Deliverable | v4.0 | 0/TBD | Not started | - |
| 23. OWASP Security Agent | v4.0 | 0/TBD | Not started | - |
| 24. Documentation & Final Verification | v4.0 | 0/TBD | Not started | - |
