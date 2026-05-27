"""
Renovate AI triage — fetches a Renovate PR diff, sends it to the Claude API
using the renovate-review skill as the system prompt, and posts the result
as a PR comment. Invoked by .github/workflows/renovate-triage.yml.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import anthropic


def run(cmd: list[str], **kwargs) -> str:
    """Run a subprocess and return stdout. Raises on non-zero exit."""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        **kwargs,
    )
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def fetch_pr_metadata(repo: str, pr_number: str) -> dict:
    """Fetch PR title, state, and branch info."""
    raw = run([
        "gh", "api",
        f"repos/{repo}/pulls/{pr_number}",
        "--jq", "{title, state, base: .base.ref, head: .head.ref, body}",
    ])
    return json.loads(raw)


def fetch_pr_files(repo: str, pr_number: str) -> list[dict]:
    """Fetch changed files with patches."""
    raw = run([
        "gh", "api",
        f"repos/{repo}/pulls/{pr_number}/files",
        "--jq", "[.[] | {filename, additions, deletions, patch}]",
    ])
    return json.loads(raw)


def load_skill(repo_root: Path) -> str:
    """Load the renovate-review skill as the system prompt."""
    skill_path = repo_root / ".claude" / "skills" / "renovate-review" / "SKILL.md"
    if not skill_path.exists():
        print(f"Skill not found at {skill_path}", file=sys.stderr)
        sys.exit(1)
    return skill_path.read_text()


def build_user_message(pr_number: str, metadata: dict, files: list[dict]) -> str:
    """Construct the user turn sent to the model."""
    files_block = json.dumps(files, indent=2)
    return (
        f"Review PR #{pr_number}.\n\n"
        f"## PR Metadata\n```json\n{json.dumps(metadata, indent=2)}\n```\n\n"
        f"## Changed Files\n```json\n{files_block}\n```\n\n"
        "Run the skill end-to-end. This is a fully autonomous run — "
        "do NOT ask for approval, do NOT apply fixes, do NOT edit any files. "
        "Output only the risk matrix report as specified in Step 6, "
        "prefixed with the line: **Automated Renovate review**"
    )


def call_claude(system_prompt: str, user_message: str) -> str:
    """Call the Anthropic API and return the response text."""
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    text_blocks = [b for b in message.content if b.type == "text"]
    if not text_blocks:
        print("No text block in Claude response", file=sys.stderr)
        sys.exit(1)
    return text_blocks[0].text


def post_comment(repo: str, pr_number: str, body: str) -> None:
    """Write LLM output to a temp file and pipe it to gh pr comment.

    LLM output is treated as untrusted text — it is never eval'd or passed
    as a shell argument. Writing to a temp file and using --body-file keeps
    it out of the process argument list entirely.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(body)
        tmp_path = f.name

    try:
        run([
            "gh", "pr", "comment", pr_number,
            "--repo", repo,
            "--body-file", tmp_path,
        ])
    finally:
        os.unlink(tmp_path)


def main() -> None:
    repo = os.environ["REPO"]
    pr_number = os.environ["PR_NUMBER"]

    # Validate PR number is purely numeric before using in API calls.
    if not pr_number.isdigit():
        print(f"Invalid PR_NUMBER: {pr_number!r} — must be numeric", file=sys.stderr)
        sys.exit(1)

    repo_root = Path(__file__).parent.parent

    print(f"Fetching PR #{pr_number} from {repo}...")
    metadata = fetch_pr_metadata(repo, pr_number)
    files = fetch_pr_files(repo, pr_number)

    print("Loading skill...")
    system_prompt = load_skill(repo_root)

    print("Calling Claude API...")
    user_message = build_user_message(pr_number, metadata, files)
    report = call_claude(system_prompt, user_message)

    print("Posting comment...")
    post_comment(repo, pr_number, report)
    print("Done.")


if __name__ == "__main__":
    main()
