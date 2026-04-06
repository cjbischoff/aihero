# VSCode/Cursor Setup

## For Reviewers & Contributors

### Quick Start

1. **Open the root folder**:
   ```bash
   code .
   ```

2. **Copy example settings** (first time only):
   ```bash
   cp .vscode/settings.example.json .vscode/settings.json
   ```

3. **Install recommended extensions** (prompted on first open):
   - Python
   - Pylance
   - Jupyter
   - Ruff

### Setup Virtual Environments

```bash
# Course environment
cd course/
uv sync

# Project environment
cd ../project/
uv sync
```

### Python Interpreter Switching

**Default:** `project/.venv/bin/python` (has pre-commit hooks)

**When working in course/ notebooks:**
- Cmd/Ctrl + Shift + P → "Python: Select Interpreter"
- Choose `course/.venv/bin/python`

### File Structure

- `settings.example.json` - Template settings (committed)
- `extensions.json` - Recommended extensions (committed)
- `settings.json` - Your personal settings (gitignored)
- `README.md` - This file (committed)

### Project Context Notes

- **course/** - Learning-focused, no pre-commit hooks
- **project/** - Production standards, pre-commit hooks enabled
- **.planning/** - GSD workflow artifacts, visible in explorer
