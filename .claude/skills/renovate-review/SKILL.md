---
name: renovate-review
description: Use when reviewing a Renovate dependency-bump PR to investigate breaking changes, known CVEs, exploitability, upgrade complexity, and test coverage before merge
allowed-tools: Bash(gh api:*), Bash(gh pr view:*), Bash(gh auth status:*), Bash(ls:*), Bash(cat:*), Read, Grep, Glob, Edit
version: 2.0.0
---

# Renovate PR Review

Investigate a Renovate-generated dependency-bump PR across four dimensions:
1. **Security** — known CVEs in the old version; CVSS score and exploitability
2. **Risk** — breaking changes, dead deps, deprecated config patterns
3. **Upgrade complexity** — effort required to safely land the new version
4. **Test coverage** — whether the repo has tests and whether they cover the bumped packages

Works across all sub-projects in cjbischoff/aihero (app, course, project).

## Core Principle

A Renovate PR is a proposal, not a ground truth. The right question for every bump is not
"did the version number change?" but "what does this change mean for the code that runs in
production, and how confident can I be that tests will catch a regression?" This skill
formalizes that investigation so it is reproducible instead of tribal knowledge.

## Constraints

- **Read-only until approval.** Investigate first, propose fixes with diffs, wait for the
  user to say "apply" before editing anything.
- **Never commit, never push, never run builds.** Suggest verification commands; do not
  execute them. The only exceptions are `gh api` read calls and `cat` on local files.
- **Never modify `uv.lock` manually.** If deps change, the user re-runs `uv sync`.
- **Never modify `renovate.json5`.** Do not suggest grouping changes.

## Workflow

### Step 1: Fetch the PR

Accept a PR number or URL as argument. If a full GitHub URL is given, extract the number.

```bash
gh auth status
```

If not authenticated, tell the user to authenticate first and stop.

Fetch PR metadata and changed files:

```bash
gh api repos/cjbischoff/aihero/pulls/<PR> --jq '{title, state, base: .base.ref, head: .head.ref, body}'
gh api repos/cjbischoff/aihero/pulls/<PR>/files --jq '.[] | {filename, additions, deletions, patch}'
```

**If the PR body is truncated** (Renovate often hits GitHub's 65K character limit — look for
`"This PR body was truncated"`), rely on the `patch` field of the dep manifest file for the
authoritative diff. Do not trust the PR body summary.

### Step 2: Detect Stack and Project

**Stack detection** — aihero is Python-only. Confirm by checking changed filenames:
`pyproject.toml` or `requirements.txt` → Python flow.

**Project detection** — read `.github/labeler.yml` and match the changed file paths against
the glob patterns to identify the `component-*` label. Extract the app path:

| Label               | App root  |
| ------------------- | --------- |
| `component-app`     | `app/`    |
| `component-course`  | `course/` |
| `component-project` | `project/`|

If multiple `component-*` labels are matched, stop and ask the user which one to analyze.
Non-component labels (`ci-cd`) alongside a single component label are fine — ignore them.

### Step 3: Parse Bumps and Classify by Risk

From the dep manifest `patch`, extract every `"<pkg>": "<old>" -> "<pkg>": "<new>"` line.
Build a structured list: `{name, old, new, dev}`.

**Risk tiers:**

| Tier       | Criteria                                                                                                                                     |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **High**   | Major semver bump (`1.x -> 2.x`), any `0.x -> 0.y` bump, framework packages (FastAPI, SQLAlchemy, Pydantic, pydantic-ai, openai, streamlit) |
| **Medium** | Minor bumps on packages with a documented history of breakage on minors (groq, sentence-transformers pre-1.0)                                |
| **Low**    | Patch bumps, dev-only tooling, ordinary minor bumps on stable packages                                                                       |

Any package with a **known CVE in the old version is automatically elevated to High**,
regardless of semver distance. A CVE on a package that is network-reachable or handles
untrusted input escalates further to **Critical** — flag it prominently at the top of the
report.

Do not mechanically escalate based on raw version-number distance. A large jump on a
well-behaved package is still Low if the semver type is a minor bump. Risk comes from what
the package *does*, its track record, and its exposure to untrusted input.

### Step 4: CVE and Exploitability Assessment

For **every bumped package**, check against your training data for known security advisories
affecting the **old version**. Note:

- CVE ID(s) and brief description
- CVSS base score and severity rating (Critical / High / Medium / Low)
- **Attack vector** — Network, Adjacent, Local, or Physical
- **Privileges required** — None, Low, or High
- **User interaction** — None or Required
- **Exploitability** — is there a known proof-of-concept or active exploitation in the wild?
- Whether the new (bumped) version resolves the CVE

**Exploitability framing to apply:**

| Signal | Implication |
| ------ | ----------- |
| Network-reachable, no auth required | Highest urgency — likely exploitable by any internet actor |
| Network-reachable, auth required | High urgency — reduces attack surface to authenticated users |
| Requires local access | Lower urgency unless multi-tenant or shared infrastructure |
| Active exploitation in the wild | Treat as Critical regardless of CVSS |
| PoC exists but no active exploitation | High urgency — exploitation is feasible |
| No PoC known | Standard urgency — apply timeline based on CVSS |

**Training data caveat:** Always append to the security section:
> "CVE data sourced from model training data (cutoff Aug 2025). Verify at
> **osv.dev/pypi/\<pkg\>** or **github.com/advisories** before merging."

If no CVEs are found in training data, output: `No known CVEs (verify at osv.dev)`.

### Step 5: Verify Usage and Upgrade Complexity

**For every High-risk bump:**

1. **Grep source for imports** using the patterns below. Read every match to understand how
   the package is used.
2. **If zero results:** flag as **dead dep**. Fix candidate.
3. **If used:** parse `uv.lock` in the app root for the exact resolved version.
4. **Query Context7** for documented breaking changes — only for framework bumps and 0.x
   bumps. Skip for minor bumps to avoid unnecessary token cost.
5. **Assess upgrade complexity** (see below).

**For every Medium-risk bump:** Grep only. Flag if dead. Skip Context7. Assess complexity.

**For every Low-risk bump:** Skip investigation. Group in a one-line "safe bumps" footer.
If a Low-risk bump has a known CVE, elevate it and investigate fully.

#### Python grep patterns

```
^import <pkg>           # top-level import
^from <pkg>[. ]         # from x import y / from x.submod import y
```

Note that PyPI names and import names often differ. Key mappings for this repo:

| PyPI name            | Python import |
| -------------------- | ------------- |
| `python-frontmatter` | `frontmatter` |
| `pydantic-ai`        | `pydantic_ai` |
| `pyyaml`             | `yaml`        |
| `pillow`             | `PIL`         |
| `beautifulsoup4`     | `bs4`         |
| `psycopg2-binary`    | `psycopg2`    |
| `python-dotenv`      | `dotenv`      |

When in doubt, check the package's PyPI page or `pyproject.toml` entry-points.

#### Upgrade complexity rating

For every package that is actively used, classify the effort to safely land the upgrade:

| Rating | Meaning |
| --- | --- |
| **Minimal** | No API changes; pure bugfix or security backport. Drop-in replacement. |
| **Moderate** | Some deprecations or renamed symbols; migration guide exists; changes are mechanical. Estimated: under 1 hour. |
| **Significant** | Breaking API changes affecting actively used symbols; requires code edits before the app will function. Estimated: half-day or more. |

Determine the rating by:
- Checking the changelog or migration guide via Context7 (for framework bumps)
- Grepping for symbols known to have changed and checking if the codebase uses them
- Noting any required manual steps (config file format changes, environment variable renames, etc.)

For **Minimal** and **Moderate** upgrades, briefly state why (e.g., "only internal refactor,
public API unchanged" or "one renamed method, not used in this codebase").

For **Significant** upgrades, list the specific symbols or behaviors that changed and which
source files are affected.

### Step 6: Test Coverage Assessment

Before emitting the risk matrix, check whether the app root has automated tests and whether
the bumped packages appear in them.

```bash
# Discover test files
find <app-root> -name "test_*.py" -o -name "*_test.py" | head -20
ls <app-root>/tests/ 2>/dev/null
ls <app-root>/test/ 2>/dev/null
```

**If no test files found:**
> ⚠️ **No test files detected in `<app-root>/`.** This upgrade carries elevated regression
> risk — there is no automated safety net. Manual smoke testing is required before merging.

**If test files found:** For each High/Medium-risk bump, grep for the package's import name
in the test files to determine whether tests exercise it.

```bash
grep -rn "import <pkg>\|from <pkg>" <app-root>/tests/ --include="*.py"
```

Report for each actively-used bump whether tests cover it:

| Package | Tests cover it? | Notes |
| ------- | --------------- | ----- |
| `openai` | Yes — 3 test files | `test_chat.py`, `test_embeddings.py`, `test_stream.py` |
| `minsearch` | No | Package is used in `search.py` but no test covers that module |

A package in active use with no test coverage is a **higher-risk merge** — say so explicitly.

### Step 7: Deprecated-Config Scan

When a framework bump is present, check for known deprecation patterns. Add new patterns
here as they are encountered.

#### Python framework bumps (FastAPI, Pydantic, SQLAlchemy, pydantic-ai)

Not yet fully characterized — add specific rules here as they are encountered. For now, on
major bumps, emit a "manual migration guide required" note and link to the framework's
upgrade docs via Context7.

#### openai SDK bumps

The openai Python SDK has had multiple breaking changes between major versions. On a major
bump, grep for deprecated client instantiation patterns:

```bash
grep -rn "openai.ChatCompletion" <app-root> --include="*.py"
grep -rn "openai.Completion" <app-root> --include="*.py"
```

These patterns were removed in openai v1.0. Flag any matches as [MIGRATE].

### Step 8: Emit Risk Matrix

Output a structured report. Use this format exactly:

```markdown
## PR #<num> -- <title>

**Stack:** Python · **Project:** <component-name> · **App root:** `<path>` · **Status:** <open | merged | closed>

---

### 🔒 Security Advisories

| Package | Old version | CVE | CVSS | Severity | Attack vector | Exploitability | Fixed in |
| ------- | ----------- | --- | ---- | -------- | ------------- | -------------- | -------- |
| `requests` | 2.31.0 | CVE-2024-35195 | 5.6 | Medium | Network | No known PoC | 2.32.4 |

> CVE data from model training data (cutoff Aug 2025). Verify at osv.dev/pypi/<pkg> or github.com/advisories.

*(If no advisories found: "No known CVEs for packages in this PR — verify at osv.dev.")*

---

### High-risk bumps

| Package | Change | Resolved | Complexity | Verdict | Evidence |
| ------- | ------ | -------- | ---------- | ------- | -------- |
| `pydantic-ai` | `0.x -> 1.0` | `1.0.2` | Significant — 3 removed methods used in app/ | `[VERIFY]` | Used in app/search_agent.py:12 |
| `openai` | `1.x -> 2.x` | `2.x.x` | Minimal — no deprecated patterns found | `[SAFE]` | No deprecated patterns found |

### Medium-risk bumps

| Package | Change | Complexity | Verdict | Evidence |
| ------- | ------ | ---------- | ------- | -------- |
| `groq` | `0.8 -> 0.9` | Minimal | `[SAFE]` | Imports found, API unchanged per docs |

### Low-risk bumps (not investigated)

`requests 2.32.0->2.33.1`, `structlog 25.4.0->25.5.0`, <...>

---

### 🧪 Test Coverage

| Package | In use | Tests cover it | Risk note |
| ------- | ------ | -------------- | --------- |
| `openai` | Yes | Yes — test_chat.py, test_embeddings.py | Regression likely caught |
| `minsearch` | Yes | **No** | No tests cover search.py — manual verification required |

*(or: "⚠️ No test files found in app/ — all upgrades carry elevated regression risk.")*

---

### Deprecated-config findings

- (none found) or list specific file:line findings here

### Proposed fixes (awaiting approval)

[show diffs here — see Step 9]

---

**Verdict legend:**
- `[SAFE]` — investigated, no action needed
- `[VERIFY]` — cannot be determined statically; run the verification command
- `[DEAD]` — unused dep, safe to remove
- `[MIGRATE]` — breaking change in active use; user must manually update code
- `[CVE]` — known vulnerability in old version; upgrade is a security fix
- `[RESOLVED]` — issue was valid but already fixed in the working tree
- `[UNKNOWN]` — investigation inconclusive; user should review manually
```

Use bracketed text labels, not emoji (except the section headers above which use emoji for
visual scan-ability in GitHub PR comments).

### Step 9: Propose Fixes and Verification

Propose fix diffs for everything mechanical. Show them as code blocks labeled with the
target file. Do NOT call `Edit` yet.

Categories of mechanical fixes:
1. **Dead deps** — remove lines from `pyproject.toml` `[project.dependencies]`
2. **Deprecated config options** — per Step 7 findings
3. **Non-functional scripts** — remove broken entry-points or scripts

For `[VERIFY]` items, provide the exact command the user should run to confirm safety:

```bash
# Example verification command for minsearch API stability
python -c "from minsearch import Index, VectorSearch; print('API intact')"
```

For each proposed fix, write a clear before/after. Then stop and say:

> "Ready to apply these fixes? Reply `apply` to write them, or tell me which ones to skip."

Only after explicit approval, use `Edit` to apply them. Do not call `git add` or `git commit`.

## Output

The skill's final output in the chat is:
1. Security advisories section (Step 8)
2. Risk matrix with complexity column (Step 8)
3. Test coverage table (Step 8)
4. Deprecated-config findings (Step 7, inline in the matrix)
5. Proposed fix diffs (Step 9)
6. The approval prompt

No narrative summary, no "I found N issues", no hedging.

## Edge Cases

**PR body is truncated by GitHub.** Always parse the `patch` field — do not rely on the PR body.

**Multiple projects touched.** Stop and ask the user which one to analyze.

**PR already merged.** Warn the user and ask if they still want the report. If they proceed,
set `Status: merged` in the report header and use `[RESOLVED]` for findings already fixed.

**`gh` not available.** Ask the user to run `gh auth status` manually. Offer to analyze if
the user pastes the `pyproject.toml` diff manually.

**No dep manifest in the diff.** This is not a Renovate dep PR. Stop and say the skill does
not apply.

**Pre-1.0 Python package with a minor bump.** Treat as High-risk.

**Transitive-only package.** If a package appears in the diff but has no source imports AND
no entry in `pyproject.toml`, it is transitive. Ignore it.

**CVE affects old version but new version also has a CVE.** Flag both — the upgrade fixes
one issue but the recommended version may itself be vulnerable. Recommend the earliest
fully-patched version instead.

**No tests and significant upgrade complexity.** Make this the top-line finding:
> ⚠️ **High regression risk:** `<pkg>` has Significant upgrade complexity and `<app-root>/`
> has no automated tests. Do not merge without manual end-to-end verification.

## What This Skill Does NOT Do

- Does not run builds, typecheckers, tests, or container actions
- Does not batch-review multiple PRs in one call — one PR per invocation
- Does not touch `renovate.json5` or suggest grouping changes
- Does not commit, push, or create follow-up PRs
- Does not install or upgrade packages directly — only edits manifest files on approval
- Does not make live network requests to CVE databases — uses training data only (caveat always shown)
