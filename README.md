# Xero FinOps

CLI tools to manage Xero accounting data, automate journal entries, and generate financial reports via the Xero API.

## Install

To use these scripts, you need to create a Xero App to get your API credentials (`CLIENT_ID` and `CLIENT_SECRET`).

1. Go to [Xero Developer Portal](https://developer.xero.com/app/manage/) and create a new app.
2. Select "Web app" as the integration type.
3. Set the Redirect URI to `http://localhost:8888/callback`.
4. Copy `xero_config.example.yaml` to `xero_config.yaml` and fill in your credentials.

## Scripts

All executable scripts now live under the `scripts/` directory. Run them with `uv` or `python` using their full path
(for example, `uv run scripts/xero_journal_manager.py --help`).

### `scripts/xero_journal_manager.py`

Manage Xero Manual Journals via the API.

- **View**: List journals with powerful filtering (e.g., by AccountCode, Amount, Date).
- **Edit**: Fix incorrect journal entries (e.g., reassigning Account Codes for loan repayments).

### `scripts/xero_coa_manager.py`

Manage the Xero Chart of Accounts.

- **View**: List all accounts in the ledger.
- **Filter**: Search for specific accounts by code, name, or class.

### `scripts/xero_pnl_report.py`

Generate financial reports directly from the CLI.

- **Profit & Loss**: Fetch P&L for any custom date range.

### `scripts/xero_balance_sheet_report.py`

Generate Balance Sheet reports.

- **Balance Sheet**: Fetch Balance Sheet for any specific date.

### `scripts/xero_connect.py`

Handle authentication with the Xero API.

- **Connect**: Authenticate and generate the `.xero_token.json` file required by other scripts.

## Development

### Setup

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Install Python dependencies (for devcontainer)
pip install -r .devcontainer/requirements.txt
```

### Testing and Validation

```bash
# Run all pre-commit checks
pre-commit run -a

# Run specific checks
pre-commit run markdownlint -a
pre-commit run yamllint -a
pre-commit run black -a
pre-commit run flake8 -a
```

## AI Agents

This repository provides AI agent configurations for automated development.

### Agent Configuration Files

| File/Directory | Audience | Purpose |
| -------------- | -------- | ------- |
| [AGENTS.md](AGENTS.md) | All agents | Repository-specific guidance and workflows |
| [CLAUDE.md](CLAUDE.md) | Claude | Claude-specific configuration |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Copilot | Coding standards and project context |
| [.github/agents/](.github/agents/) | Orchestrators | Specialized agent configs for specific tasks |
| [.github/skills/](.github/skills/) | All agents | Reusable capabilities (git, GitHub Actions, etc.) |
| [.github/prompts/](.github/prompts/) | All | Automation prompt templates |
| [.github/instructions/](.github/instructions/) | Linters & agents | Language-specific code standards |

See also:

- [`AGENTS.md` file format specification](https://agents.md/)
- [Best practices for using GitHub Copilot](https://gh.io/copilot-coding-agent-tips).


## GitHub Actions

For documentation on GitHub Actions workflows, problem matchers, and CI/CD
configuration, see [.github/README.md](.github/README.md).
