# VS Code Tours

This directory contains interactive code tours for exploring and understanding
this repository's structure, features, and conventions.

## What are Code Tours?

Code tours are guided walkthroughs that help you navigate through a codebase
step-by-step. Each tour highlights specific files, directories, and code
sections with explanatory descriptions, making it easier to:

- Onboard new contributors
- Understand complex workflows
- Learn project conventions and standards
- Discover key features and configurations

## Using Code Tours

### Prerequisites

Install the **CodeTour** extension for Visual Studio Code:

- **Extension ID**: `vsls-contrib.codetour`
- **Marketplace**: [CodeTour Extension](https://marketplace.visualstudio.com/items?itemName=vsls-contrib.codetour)
- **Installation**: Search for "CodeTour" in the VS Code Extensions view or
  click the marketplace link

### Starting a Tour

1. Open this repository in VS Code
2. Look for the CodeTour icon in the Activity Bar (left sidebar)
3. Click on a tour from the list to begin
4. Use the navigation controls to step through the tour

Alternatively, open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and
type "CodeTour: Start Tour" to select a tour.

## Available Tours

### Getting Started

**File**: `getting-started.tour`

A walkthrough covering:

- Repository overview and purpose
- Python CLI scripts for Xero API management
- Configuration files and credentials setup
- GitHub Actions workflows
- Coding standards and formatting guidelines
- Development container setup

**Recommended for**: New contributors and anyone wanting to understand how to
use and contribute to the Xero FinOps tools.

## Creating New Tours

To create or update tours, refer to the
[code-tour.agent.md](../.github/agents/code-tour.agent.md) agent documentation,
which provides comprehensive guidance on CodeTour best practices and schema.

Key considerations:

- Use descriptive titles and step names
- Follow a logical flow (high-level to detailed)
- Include context and explanations in step descriptions
- Store tours in this `.tours` directory
- Keep tours up-to-date when making significant changes to the codebase

## Additional Resources

- [CodeTour Documentation](https://github.com/microsoft/codetour)
- [CodeTour Schema](https://aka.ms/codetour-schema)
- [Agent Documentation](../.github/agents/code-tour.agent.md)
