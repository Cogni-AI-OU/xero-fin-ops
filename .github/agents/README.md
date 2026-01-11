# Custom Agents

This folder contains custom agents designed to enhance your development workflow.
These agents are tailored to specific tasks and integrate seamlessly with GitHub Copilot and MCP servers.

## Available Agents

### [Copilot Plus](copilot-plus.agent.md)

Enhanced agent with critical thinking, robust problem-solving, and context-aware resource management. Features:

- Automatic file size checking before viewing
- Smart filtering for long outputs
- Command installation fallback logic
- Self-improvement capabilities
- Never-give-up problem-solving approach

### [Code Tour Expert](code-tour.agent.md)

Expert agent for creating and maintaining VSCode CodeTour files. Features:

- Create comprehensive `.tour` JSON files
- Design step-by-step codebase walkthroughs
- Implement proper file references and directory steps
- Configure tour versioning with git refs
- Best practices for tour organization

## How to Use Custom Agents

### Installation

- Download the desired agent configuration file (`*.agent.md`) and add it to your repository.
- Use the Copilot CLI for local testing: [Copilot CLI](https://gh.io/customagents/cli).

### Activation

- Merge the agent configuration file into the default branch of your repository.
- Access installed agents through the VS Code Chat interface, Copilot CLI, or assign them in CCA.

## Reference Documentation

For more details, see:

- [About custom agents](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-custom-agents)
- [Create custom agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [Customizing the development environment][customize-env]
- [Customizing or disabling the firewall][firewall-config]

For a collection of awesome custom agents, visit the
[GitHub Awesome Copilot repository](https://github.com/github/awesome-copilot).

## Security Considerations

### Claude Code Agent Git Access

When using Claude Code (triggered via `@claude` in comments), the agent has broad
git access via `Bash(git:*)` to enable autonomous code changes. This requires
proper repository safeguards.

**Access controls in place:**

- Only trusted users (OWNER, MEMBER, COLLABORATOR, CONTRIBUTOR) can trigger Claude
- PR/issue authors can only trigger Claude on their own content
- External contributors are explicitly blocked

**Required repository protections:**

Repository administrators must configure:

1. **Branch protection rules** on main/protected branches requiring PR reviews and status checks
2. **GitHub audit log monitoring** for `github-actions[bot]` commit activity
3. **CODEOWNERS** files for sensitive directories requiring specific approvals

**Best practices:**

- Review Claude's commits before merging PRs
- Use draft PRs for Claude's work requiring explicit promotion
- Monitor workflow logs for unexpected behavior
- Rotate `ANTHROPIC_API_KEY` periodically

See [.github/README.md](../README.md#security) for detailed security configuration.

<!-- Named links -->

[customize-env]: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-environment
[firewall-config]: https://gh.io/copilot/firewall-config
