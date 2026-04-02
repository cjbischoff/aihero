---
phase: 13-dependencies-setup
plan: 01
subsystem: dependencies
tags: [dependencies, minsearch, sentence-transformers, torch, day3]
dependency_graph:
  requires: [pyproject.toml (Day 2)]
  provides: [search dependencies, embedding infrastructure foundation]
  affects: [Phase 14 (text search), Phase 15 (vector search), Phase 16 (hybrid search)]
tech_stack:
  added:
    - minsearch==0.0.10 (text and vector search library)
    - sentence-transformers==5.3.0 (semantic embedding generation)
    - torch==2.11.0 (PyTorch backend, CPU-only, resolved from >=2.0.0)
    - 22 transitive dependencies (numpy, scipy, scikit-learn, transformers, huggingface-hub, etc.)
  patterns:
    - Dual environment sync (course/ and project/ receive identical dependencies)
    - Exact version pins for reproducibility (minsearch, sentence-transformers)
    - Minimum version constraint for flexibility (torch >=2.0.0)
    - Hash-pinned lockfiles for supply chain security
key_files:
  created: []
  modified:
    - course/pyproject.toml (added 3 dependencies)
    - course/uv.lock (resolved 170 packages)
    - course/requirements.lock (regenerated with hashes, 93KB)
    - project/pyproject.toml (added 3 dependencies)
    - project/uv.lock (resolved 175 packages)
    - project/requirements.lock (regenerated with hashes, 93KB)
decisions:
  - decision: "Used uv add command per D-08"
    rationale: "Atomically updates pyproject.toml and syncs environment in single operation"
    alternatives_considered: ["Manual pyproject.toml edit + uv sync"]
  - decision: "Resolved torch to 2.11.0 from >=2.0.0 constraint"
    rationale: "Latest stable version, meets minimum requirement, CPU-only sufficient for course scale"
    alternatives_considered: ["Pin to 2.0.0 exactly (unnecessary constraint)"]
  - decision: "Regenerated requirements.lock after uv add"
    rationale: "Maintains hash-pinned lockfile pattern from Phase 7, ensures reproducibility"
    alternatives_considered: ["Skip lockfile regeneration (breaks reproducibility)"]
metrics:
  duration_seconds: 163
  duration_human: "2 min 43 sec"
  tasks_completed: 2
  files_modified: 6
  commits: 2
  dependency_packages_added: 27
  lockfile_size_kb: 93
completed_date: "2026-04-02"
---

# Phase 13 Plan 01: Install Day 3 Search Dependencies Summary

**One-liner:** Installed minsearch 0.0.10, sentence-transformers 5.3.0, and torch 2.11.0 for text/vector search with hash-pinned reproducibility across both course and project environments.

## What Was Built

Established the dependency foundation for Day 3 search work by installing three core libraries across both course/ and project/ environments:

1. **minsearch 0.0.10** - Course-specified library for text (TF-IDF) and vector search operations
2. **sentence-transformers 5.3.0** - Hugging Face library for semantic embedding generation (supports all-MiniLM-L6-v2 model)
3. **torch 2.11.0** - PyTorch backend for sentence-transformers inference (CPU-only, resolved from >=2.0.0 constraint)

These dependencies enable all of Phase 14 (text search), Phase 15 (vector search), and Phase 16 (hybrid search) implementations.

## Tasks Executed

### Task 1: Add Day 3 search dependencies using uv add (Commit: 8a6c6e4)

**Action:** Ran `uv add` in both course/ and project/ directories with exact version pins per locked decisions D-01 through D-05.

**Results:**
- course/ environment: Resolved 170 packages, installed 27 new packages (including 22 transitive dependencies)
- project/ environment: Resolved 175 packages, installed 22 new packages (torch and dependencies already cached from course/)
- Both pyproject.toml files updated with minsearch==0.0.10, sentence-transformers==5.3.0, torch>=2.0.0
- All imports verified working: `import minsearch`, `from sentence_transformers import SentenceTransformer`, `import torch`
- torch version confirmed >= 2.0.0 requirement (resolved to 2.11.0)

**Key transitive dependencies:**
- numpy 2.4.4 (numerical operations)
- scipy 1.17.1 (scientific computing)
- scikit-learn 1.8.0 (TF-IDF implementation for minsearch)
- transformers 5.5.0 (Hugging Face model loading)
- huggingface-hub 1.8.0 (model download and caching)
- tokenizers 0.22.2 (fast tokenization for transformers)

**Download note:** torch is a large package (~77MB download, ~200MB installed). The initial install took ~6 seconds for download and ~383ms for installation. Subsequent operations in project/ reused the cached packages.

### Task 2: Regenerate requirements.lock files with hash-pinned dependencies (Commit: 6367f61)

**Action:** Ran `uv pip compile pyproject.toml --generate-hashes --output-file requirements.lock` in both course/ and project/ directories following Phase 7 pattern.

**Results:**
- course/requirements.lock: Regenerated with 170 packages, all with sha256 hashes (~93KB)
- project/requirements.lock: Regenerated with 175 packages, all with sha256 hashes (~93KB)
- Both lockfiles contain minsearch==0.0.10, sentence-transformers==5.3.0, torch==2.11.0 with hashes
- Lockfile size increased significantly from ~10KB to ~93KB due to torch's extensive dependency tree (expected and documented in plan)

**Hash verification sample:**
```
minsearch==0.0.10 \
    --hash=sha256:...
sentence-transformers==5.3.0 \
    --hash=sha256:...
torch==2.11.0 \
    --hash=sha256:...
```

## Deviations from Plan

None - plan executed exactly as written. All locked decisions (D-01 through D-08) were followed precisely.

## Verification Results

All success criteria met:

1. ✅ `uv add` succeeded in both course/ and project/ directories (per D-08)
2. ✅ Both pyproject.toml files contain minsearch==0.0.10, sentence-transformers==5.3.0, torch>=2.0.0
3. ✅ `import minsearch` succeeds in both environments
4. ✅ `from sentence_transformers import SentenceTransformer` succeeds in both environments
5. ✅ `import torch` succeeds in both environments with version 2.11.0 >= 2.0.0
6. ✅ Both requirements.lock files regenerated with hash-pinned dependencies
7. ✅ Existing configurations preserved (tool.ruff, tool.black, etc. in project/)
8. ✅ Existing dependencies preserved (tiktoken, openai, groq from Day 2)

## Technical Notes

### uv add Workflow (Decision D-08)

The `uv add` command provides an atomic workflow that:
1. Updates pyproject.toml with specified version constraints
2. Resolves all transitive dependencies
3. Updates uv.lock with resolved versions
4. Installs packages into the virtual environment

This is superior to manual pyproject.toml editing because it guarantees consistency between the dependency declaration, the lockfile, and the installed packages in a single operation.

### torch Version Resolution

Per decision D-05, torch was specified with minimum version constraint `>=2.0.0` rather than exact pin. This provides flexibility for minor/patch updates while maintaining stability at the major version level. The resolver chose torch 2.11.0 (latest stable as of 2026-04-02), which meets the requirement and provides best compatibility with sentence-transformers 5.3.0.

### Dependency Tree Analysis

The 27 packages installed in course/ break down as:
- **Core libraries** (3): minsearch, sentence-transformers, torch
- **Numerical stack** (4): numpy, scipy, scikit-learn, pandas
- **Transformers ecosystem** (5): transformers, tokenizers, huggingface-hub, safetensors, hf-xet
- **Utilities** (8): click, filelock, fsspec, joblib, rich, shellingham, typer, annotated-doc
- **Math/graph** (3): sympy, mpmath, networkx
- **Text rendering** (2): markdown-it-py, mdurl
- **Build tools** (2): setuptools, threadpoolctl

All are legitimate transitive dependencies with clear provenance chains visible in requirements.lock.

### Lockfile Size Growth

The requirements.lock files grew from ~10KB (Day 2) to ~93KB (Day 3) - a 9x increase. This is entirely due to torch's extensive dependency tree and is expected. The hash-pinned lockfiles ensure:
- Supply chain security (every package hash-verified)
- Reproducibility across environments
- Audit trail for dependency provenance

## Readiness for Phase 14

All Phase 14 prerequisites are now satisfied:

- ✅ minsearch library available for TF-IDF indexing
- ✅ scikit-learn available as minsearch backend
- ✅ numpy/scipy available for numerical operations
- ✅ Both environments synchronized with identical dependencies
- ✅ Hash-pinned lockfiles ensure reproducible installations

Phase 15 prerequisites also satisfied:

- ✅ sentence-transformers available for embedding generation
- ✅ torch backend installed for CPU inference
- ✅ huggingface-hub configured for model downloads

No additional dependency work needed before implementing search functionality.

## Known Issues

None. All verification checks passed, no errors encountered, no warnings requiring attention.

## Next Phase

Phase 14: Text Search Foundation - Implement lexical search with minsearch TF-IDF scoring and field boosting.
