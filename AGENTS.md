# AGENTS.md

Guidance for Claude automation agents working in this repository.

## Quick Start

- See [README.md](README.md) for setup and installation instructions
- For enhanced agent capabilities, see [Copilot Plus](.github/agents/copilot-plus.agent.md)

## Instructions

For detailed coding standards and formatting guidelines, refer to:

- [Copilot Instructions](.github/copilot-instructions.md) - Main coding standards

## Common Tasks

### Before commit

Before each commit change:

- Verify your expected changes by `git diff --no-color`.
- Use linting and validation tools used by project to confirm your changes meet the coding standard.
- If repo uses git hooks, run them to validate your changes.

### Linting and Validation

```bash
# Run all pre-commit checks
pre-commit run -a

# Run specific checks
pre-commit run markdownlint -a
pre-commit run yamllint -a
pre-commit run flake8 -a
```

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

### Understanding the task

- When task is not clear, check further relevant information for better clarity.
- If triggered by a short comment, check if the parent comment exists and contains further information.
- If none of above helps, and task is ambiguous, communicate to the user with potential options.

### Adding or Modifying Workflows

- Workflows in `.github/workflows/` reference remote workflows via `workflow_call`
- Test workflow changes on a feature branch before merging to main
- Use `actionlint` to validate workflow syntax locally

### Updating Coding Standards

- Update `.markdownlint.yaml`, `.yamllint`, or `.editorconfig` for linting rules
- Run `pre-commit run -a` to verify changes pass all checks

## Integrating Changes from Target Branch

Recommended way is to use the **cherry-pick workflow** to rebase your commits
on top of the updated target branch:

1. Identify your feature commits
2. Fetch the latest target branch
3. Reset your branch to target (with backup)
4. Cherry-pick your feature commits
5. Verify only your changes remain

**For detailed step-by-step instructions with commands**, see:
[`.github/skills/git/SKILL.md` - "Integrating Changes from Target Branch"](.github/skills/git/SKILL.md#integrating-changes-from-target-branch-avoiding-merge-commits)

### Key Points

- **Never** use `git merge <target-branch>` for branch integration
- **Always** create backup tags before destructive operations
- **Always** verify with `git diff` that only your changes remain
- **Use** `GIT_EDITOR=true` for non-interactive cherry-pick operations

### Critical: Using `report_progress` Tool

**CRITICAL WARNING**: The `report_progress` tool automatically rebases your branch against the remote
tracking branch. This **WILL CRASH** the session if your local history has diverged from remote.

**When Crash Occurs:**

After using `git reset --hard` to rewrite history, your local branch diverges from remote. When `report_progress`
tries to auto-rebase (e.g., 113 commits), it encounters conflicts it cannot resolve, crashing the session.

**Prevention (Choose One):**

1. **Use new branch name** after rewriting history: `git checkout -b <feature>-v2` (safest)
2. **Complete git operations manually**, then ask user for manual push (never call `report_progress` after `git reset --hard`)

**If Already Crashed:**

1. Run `git rebase --abort`
2. Create new branch: `git checkout -b <feature>-v2`
3. Push new branch: `git push origin <feature>-v2`

**Error Patterns:** `Rebasing (1/XXX)` with large numbers, `CONFLICT (content)`, session crash with `GitError`

**For complete details**, see:
[`.github/skills/git/SKILL.md` - "Working with Automation Tools"](.github/skills/git/SKILL.md#working-with-automation-tools)

## References

- Claude-specific guidance: [CLAUDE.md](CLAUDE.md)
- Main documentation: [README.md](README.md)

## Troubleshooting

### GitHub Build issues

- Use `gh` command to interact with GitHub resources. For example:

  - `gh run list --limit 3` to list recent builds.
  - `gh run view {ID} --log | rg -iw "failed|error|exit"` to look for build errors.

### Firewall issues

If you encounter firewall issues when using the GitHub Copilot Agent:

- Refer to <https://gh.io/copilot/firewall-config> for configuration details.
- If you need to allowlist additional hosts, update your firewall configuration accordingly
  and keep the list of allowed hosts in `.github/agents/FIREWALL.md` up to date.

### Linting issues

If Copilot or automated checks behave unexpectedly:

- Re-run `pre-commit run -a` locally to surface formatting or linting issues.
- Verify `.markdownlint.yaml` and `.yamllint` have not been modified incorrectly.
- If problems persist, open an issue with details of the command run and any error output.

### Shell commands issues

- Prefix shell commands with `time` to measure execution duration for better visibility.
- When command takes too long, use `timeout` or similar approach to limit execution time.
