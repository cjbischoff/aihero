# Roadmap: AI Hero - Day 1

## Overview

This roadmap delivers Day 1 of the AI Hero RAG course: a working GitHub data ingestion system that downloads repositories and extracts structured documentation. The journey progresses from environment setup through course reproduction (learning the patterns), project homework (applying to a different repo), and concluding with documentation of learnings. All phases build toward understanding how to parse GitHub documentation with frontmatter metadata—the foundation for RAG systems that answer questions about code repositories.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Environment Setup** - Verify Python 3.10+, install uv, create folder structure
- [x] **Phase 2: Course Project Initialization** - Initialize uv project in course/ folder with dependencies
- [x] **Phase 3: Core Implementation** - Implement read_repo_data() with frontmatter parsing in Jupyter notebook (completed 2026-03-30)
- [x] **Phase 4: Course Validation** - Test with DataTalks FAQ and Evidently docs repositories (completed 2026-03-30)
- [ ] **Phase 5: Project Homework** - Apply patterns to OWASP LLM Top 10 repository
- [ ] **Phase 6: Documentation & Reflection** - Document learnings and challenges

## Phase Details

### Phase 1: Environment Setup
**Goal**: Developer environment ready with Python 3.10+, uv package manager, and proper folder structure
**Depends on**: Nothing (first phase)
**Requirements**: ENV-01, ENV-02, ENV-03, ENV-04
**Success Criteria** (what must be TRUE):
  1. Python 3.10 or higher is installed and accessible via command line
  2. uv package manager is installed and responds to --version command
  3. Folder structure exists: aihero/course/ and aihero/project/ subdirectories created
  4. Developer can initialize uv projects in both folders without errors
**Plans**: 1 plan

Plans:
- [x] 01-01-PLAN.md — Verify Python/uv installation and create folder structure

### Phase 2: Course Project Initialization
**Goal**: Working uv project in course/ folder with all required dependencies installed
**Depends on**: Phase 1
**Requirements**: COURSE-01, COURSE-02
**Success Criteria** (what must be TRUE):
  1. uv project exists in course/ with valid pyproject.toml configuration
  2. Dependencies installed: requests, python-frontmatter, and jupyter (dev)
  3. Developer can start jupyter notebook server from course/ folder
  4. Python can import requests and frontmatter modules without errors
**Plans**: 1 plan

Plans:
- [x] 02-01-PLAN.md — Initialize uv project and install dependencies

### Phase 3: Core Implementation
**Goal**: Working read_repo_data() function that downloads GitHub repos and parses markdown with frontmatter
**Depends on**: Phase 2
**Requirements**: COURSE-03, COURSE-04, COURSE-05, COURSE-06, COURSE-07, COURSE-08, COURSE-09, COURSE-13, COURSE-14, DOC-03
**Success Criteria** (what must be TRUE):
  1. Jupyter notebook day1.ipynb exists with complete implementation
  2. Function read_repo_data(repo_owner, repo_name) downloads repos as zip via GitHub codeload API
  3. Function processes zip archive in-memory without writing to disk
  4. Function extracts only .md and .mdx files, ignoring other file types
  5. Function parses YAML frontmatter from each markdown file and returns structured data
  6. Notebook includes inline explanations of frontmatter concept and zip processing approach
  7. Code includes comments explaining key technical decisions
**Plans**: 1 plan

Plans:
- [x] 03-01-PLAN.md — Implement read_repo_data() function in Jupyter notebook

### Phase 4: Course Validation
**Goal**: Verified that implementation works correctly with both course-provided test repositories
**Depends on**: Phase 3
**Requirements**: COURSE-10, COURSE-11, COURSE-12
**Success Criteria** (what must be TRUE):
  1. Function successfully downloads and processes DataTalks.Club FAQ repository
  2. Function successfully downloads and processes Evidently AI docs repository
  3. Notebook displays sample outputs showing parsed data structure with content and metadata
  4. Both test cases execute without errors and return expected data formats
**Plans**: 2 plans

Plans:
- [x] 04-01-PLAN.md — Test implementation with DataTalks FAQ and Evidently docs repositories
- [x] 04-02-PLAN.md — Execute notebook from fresh kernel and commit outputs (gap closure)

### Phase 5: Project Homework
**Goal**: Apply learned GitHub ingestion patterns to OWASP LLM Top 10 repository with engineering standards
**Depends on**: Phase 4
**Requirements**: PROJ-01, PROJ-02, PROJ-03, PROJ-04, PROJ-05, PROJ-06, PROJ-07, PROJ-08
**Success Criteria** (what must be TRUE):
  1. Separate uv project exists in project/ folder with dependencies installed
  2. Jupyter notebook created for personal project implementation
  3. Implementation successfully downloads OWASP LLM Top 10 repository
  4. Parser extracts all markdown documentation from OWASP repo structure
  5. Verification confirms data extraction works despite different repo organization
  6. Notebook displays sample outputs from OWASP repository showing parsed content
**Plans**: 1 plan

Plans:
- [x] 05-01-PLAN.md — Initialize project environment and create OWASP homework notebook

### Phase 6: Documentation & Reflection
**Goal**: Documented learnings and differences between course reproduction and project homework
**Depends on**: Phase 5
**Requirements**: DOC-01, DOC-02
**Success Criteria** (what must be TRUE):
  1. Course notebook includes summary of key concepts learned
  2. Project notebook documents any differences or challenges compared to course repos
  3. Both notebooks are fully executable from top to bottom with fresh kernel
  4. Documentation explains why certain implementation choices were made
**Plans**: 1 plan

Plans:
- [ ] 06-01-PLAN.md — Add learnings summary to course notebook

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Environment Setup | 1/1 | Complete | 2026-03-30 |
| 2. Course Project Initialization | 1/1 | Complete | 2026-03-30 |
| 3. Core Implementation | 1/1 | Complete   | 2026-03-30 |
| 4. Course Validation | 2/2 | Complete | 2026-03-30 |
| 5. Project Homework | 1/1 | Complete | 2026-03-30 |
| 6. Documentation & Reflection | 0/1 | Not started | - |
