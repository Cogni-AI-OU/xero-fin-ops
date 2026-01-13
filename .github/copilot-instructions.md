# Copilot Instructions for Xero FinOps

## Project Overview

This repository contains Python CLI tools for managing Xero accounting data via the Xero API. The scripts are designed
to be run as standalone executables using `uv` for dependency management.

## Coding Standards

### Python

- Use **Python 3.11+**.
- Use `uv` script headers for dependency management:

  ```python
  #!/usr/bin/env -S uv run --script
  # /// script
  # requires-python = ">=3.11"
  # dependencies = [
  #     "xero-python",
  #     "PyYAML",
  # ]
  # ///
  ```

- Follow **PEP 8** style guidelines.
- Use `argparse` for CLI argument parsing.
- Handle `BrokenPipeError` for CLI tools that might be piped to `head` or `grep`:

  ```python
  import signal
  signal.signal(signal.SIGPIPE, signal.SIG_DFL)
  ```

### Xero API

- Use the `xero-python` SDK.
- Always load credentials from `xero_config.yaml` and `.token.json`.
- Handle API rate limits and errors gracefully.
- When updating objects (like Manual Journals), ensure you wrap them in the correct container object
  (e.g., `ManualJournals(manual_journals=[journal])`).

## Project Structure

- `scripts/xero_journal_manager.py`: View and edit manual journals.
- `scripts/xero_coa_manager.py`: Manage Chart of Accounts.
- `scripts/xero_pnl_report.py`: Generate Profit & Loss reports.
- `scripts/xero_balance_sheet_report.py`: Generate Balance Sheet reports.
- `scripts/xero_connect.py`: Authenticate and generate `.token.json`.

## Common Tasks

- **Filtering**: When implementing `view` commands, allow dynamic filtering using Python syntax
  (e.g., `eval()` with safety checks) for flexibility.
- **Dry Runs**: Always implement a `--dry-run` flag for commands that modify data.

### Testing Xero Scripts

```bash
# Test individual scripts
cd scripts/
./xero_journal_manager.py --help
./xero_coa_manager.py --help
./xero_pnl_report.py --help

# Ensure scripts are executable
chmod +x scripts/*.py
```

## Environment Setup

```bash
# Install dependencies
pip install -r .devcontainer/requirements.txt

# Install pre-commit hooks
pre-commit install

# Set up environment variables (copy from .env.example)
cp .env.example .env
# Edit .env with your Xero OAuth credentials (or use xero_config.yaml)
```

## Configuration

- **Environment Variables**: All configuration is via `FREEAGENT_*` environment variables
- **OAuth2 Flow**: Uses authorization code flow with token refresh
- **Output Formats**: Supports plain, csv, json, and yaml output formats
- **Pagination**: Built-in pagination support with configurable page size
