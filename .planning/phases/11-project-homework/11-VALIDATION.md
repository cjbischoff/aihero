---
phase: 11
slug: project-homework
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-01
---

# Phase 11 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Jupyter nbconvert --execute (notebook execution validation) |
| **Config file** | none — uses project/owasp_homework.ipynb directly |
| **Quick run command** | `jupyter nbconvert --execute --to notebook --stdout project/owasp_homework.ipynb 2>&1 \| grep -E "(error\|Error\|ERROR\|exception\|Exception)" \|\| echo "✓"` |
| **Full suite command** | `cd project && source .venv/bin/activate && op run --env-file=../.env jupyter nbconvert --execute --to notebook --inplace owasp_homework.ipynb` |
| **Estimated runtime** | ~120 seconds (LLM chunking on 10 doc subset) |

---

## Sampling Rate

- **After every task commit:** Run quick command (grep for errors in stdout)
- **After every plan wave:** Run full suite command (end-to-end notebook execution)
- **Before `/gsd:verify-work`:** Full suite must be green (all cells execute without errors)
- **Max feedback latency:** 120 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 11-01-01 | 01 | 1 | PROJ-04 | notebook | `grep -q "chunk_paragraph_with_sliding_window" project/owasp_homework.ipynb` | existing | pending |
| 11-01-02 | 01 | 1 | PROJ-04 | notebook | `grep -q "paragraph_sliding_window" project/owasp_homework.ipynb` | existing | pending |
| 11-01-03 | 01 | 1 | PROJ-07 | notebook | `grep -q "Quantitative Comparison" project/owasp_homework.ipynb` | existing | pending |
| 11-01-04 | 01 | 1 | PROJ-01-08 | traceability | `grep -q "\[x\] \*\*PROJ-08\*\*" .planning/REQUIREMENTS.md` | existing | pending |
| 11-01-05 | 01 | 1 | CLAUDE.md | commit | `git log -1 --format=%G? \| grep -q "G"` | n/a | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No Wave 0 setup needed:
- Jupyter already installed in project/.venv
- Notebook structure already exists
- All dependencies (tiktoken, openai, groq) already installed from Phase 7

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Hybrid chunking quality | PROJ-04 | Visual inspection of chunk boundaries | Review comparison table shows hybrid strategy with reasonable chunk counts and token distributions |
| Analysis completeness | PROJ-07 | Content quality assessment | Read three sections (Quantitative Comparison, Strategy Recommendation, Decision Framework) and verify they reference OWASP-specific findings |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 120s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved
