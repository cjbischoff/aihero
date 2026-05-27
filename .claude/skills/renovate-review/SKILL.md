---
name: renovate-review
description: Use when reviewing a Renovate dependency-bump PR to investigate breaking changes, dead dependencies, and deprecated configs before merge
allowed-tools: Bash(gh api:*), Bash(gh pr view:*), Bash(gh auth status:*), Bash(ls:*), Bash(cat:*), Read, Grep, Glob, Edit
version: 1.0.0
---

# Renovate PR Review

Investigate a Renovate-generated dependency-bump PR for real breaking changes, flag dead
dependencies that can be removed, and scan for deprecated config patterns introduced by
framework bumps. Works across all sub-projects in cjbischoff/aihero (app, course, project).

## Core Principle

A Renovate PR is a proposal, not a ground truth. Most bumps are safe, but majors and 0.x
bumps need evidence-based verification: does the codebase actually use the package? Did the
framework deprecate something the project still relies on? This skill formalizes that
investigation so it is reproducible instead of tribal knowledge.

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
`pyproject.toml` or `requirements.txt` -> Python flow.

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

Do not mechanically escalate based on raw version-number distance. A large jump on a
well-behaved package is still Low if the semver type is a minor bump. Risk comes from what
the package *does* and its track record, not the integer gap.

A devDep is still High if it is a major bump on a framework-adjacent tool.

### Step 4: Verify Usage

**For every High-risk bump:**

1. **Grep source for imports** using the patterns below. Read every match to understand how
   the package is used.
2. **If zero results:** flag as **dead dep**. Fix candidate.
3. **If used:** parse `uv.lock` in the app root for the exact resolved version.
4. **Query Context7** for documented breaking changes — only for framework bumps and 0.x
   bumps. Skip for minor bumps to avoid unnecessary token cost.

**For every Medium-risk bump:** Grep only. Flag if dead. Skip Context7.

**For every Low-risk bump:** Skip investigation. Group in a one-line "safe bumps" footer.

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

Resolved version check: parse `uv.lock` in the app root for the exact installed version.

### Step 5: Deprecated-Config Scan

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

### Step 6: Emit Risk Matrix

Output a structured report in the chat. Use this format exactly:

```markdown
## PR #<num> -- <title>

**Stack:** Python · **Project:** <component-name> · **App root:** `<path>` · **Status:** <open | merged | closed>

### High-risk bumps

| Package       | Change       | Resolved | Verdict    | Evidence                           |
| ------------- | ------------ | -------- | ---------- | ---------------------------------- |
| `pydantic-ai` | `0.x -> 1.0` | `1.0.2`  | `[VERIFY]` | Used in app/search_agent.py:12     |
| `openai`      | `1.x -> 2.x` | --       | `[SAFE]`   | No deprecated patterns found       |

### Medium-risk bumps

| Package | Change       | Verdict  | Evidence                              |
| ------- | ------------ | -------- | ------------------------------------- |
| `groq`  | `0.8 -> 0.9` | `[SAFE]` | Imports found, API unchanged per docs |

### Low-risk bumps (not investigated)

`requests 2.32.0->2.33.1`, `structlog 25.4.0->25.5.0`, <...>

### Deprecated-config findings

- (none found) or list specific file:line findings here

### Proposed fixes (awaiting approval)

[show diffs here -- see Step 7]

**Verdict legend:**
- `[SAFE]` -- investigated, no action needed
- `[VERIFY]` -- cannot be determined statically; run the verification command
- `[DEAD]` -- unused dep, safe to remove
- `[MIGRATE]` -- breaking change in active use; user must manually update code
- `[RESOLVED]` -- issue was valid but already fixed in the working tree
- `[UNKNOWN]` -- investigation inconclusive; user should review manually
```

Use bracketed text labels, not emoji.

### Step 7: Propose Fixes and Verification

Propose fix diffs for everything mechanical. Show them as code blocks labeled with the
target file. Do NOT call `Edit` yet.

Categories of mechanical fixes:
1. **Dead deps** -- remove lines from `pyproject.toml` `[project.dependencies]`
2. **Deprecated config options** -- per Step 5 findings
3. **Non-functional scripts** -- remove broken entry-points or scripts

For each proposed fix, write a clear before/after. Then stop and say:

> "Ready to apply these fixes? Reply `apply` to write them, or tell me which ones to skip."

Only after explicit approval, use `Edit` to apply them. Do not call `git add` or `git commit`.

## Output

The skill's final output in the chat is:
1. The risk matrix (Step 6)
2. The deprecated-config findings (Step 5, inline in the matrix)
3. The proposed fix diffs (Step 7)
4. The approval prompt

No narrative summary, no "I found N issues", no hedging.

## Edge Cases

**PR body is truncated by GitHub.** Always parse the `patch` field -- do not rely on the PR body.

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

## What This Skill Does NOT Do

- Does not run builds, typecheckers, tests, or container actions
- Does not batch-review multiple PRs in one call -- one PR per invocation
- Does not touch `renovate.json5` or suggest grouping changes
- Does not commit, push, or create follow-up PRs
- Does not install or upgrade packages directly -- only edits manifest files on approval
