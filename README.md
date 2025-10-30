# NWSL Notes - Substack Publishing Tools

A Python toolkit for publishing Jupyter notebooks and Markdown files to Substack via automated browser automation.

## Features

- **Markdown Publishing**: Convert markdown files with front-matter to Substack posts
- **Notebook Export**: Export Jupyter notebooks to markdown with YAML front-matter
- **Automated Publishing**: Uses Playwright to automate Substack's editor
- **Session Management**: Saves authentication state for future runs
- **Draft & Publish Modes**: Create drafts or publish directly
- **Image Handling**: Automatically uploads local images
- **Tag Support**: Add tags from front-matter metadata

## Installation

1. Create and activate a virtual environment:
```bash
make venv
```

2. Configure your Substack space:
```bash
cp .env.example .env
# Edit .env and set SUBSTACK_SPACE=your-subdomain
```

3. Login to Substack (one-time setup):
```bash
make substack-login
```

## Usage

### Writing Posts with AI Agents

**New!** You can now use AI agents to write Substack posts in the correct format.

```bash
# In Claude Code or similar AI assistant:
"I want to write a Substack post about [topic].
Please read .claude/prompts/substack-writer.md and write
a post following that format."
```

The agent will:
1. Read the format requirements
2. Write a properly formatted post with YAML frontmatter
3. Save it to `docs/YYYY-MM-DD-topic-name.md`
4. Help you publish it

**See [docs/WORKFLOW.md](docs/WORKFLOW.md) for complete guide**

### Publishing Markdown Files

```bash
# Create/update draft
make substack-publish FILE=docs/my-post.md

# Publish live
make substack-publish FILE=docs/my-post.md PUBLISH=true
```

### Exporting Notebooks to Markdown

```bash
make nb2md NB=notebooks/demo.ipynb OUT=docs/demo.md TITLE="My Post" TAGS="eval,analysis"
```

### Markdown Front-Matter Format

```markdown
---
title: "My Post Title"
tags: [analysis, nwsl, data]
---

Your content here...
```

## CLI Usage

The tool provides a rich CLI interface:

```bash
# Login interactively
python tools/substack/cli.py login --space your-subdomain

# Publish as draft
python tools/substack/cli.py publish docs/post.md --space your-subdomain

# Publish live
python tools/substack/cli.py publish docs/post.md --space your-subdomain --publish
```

## Project Structure

```
nwsl-notes/
├── tools/substack/          # Substack publishing tools
│   ├── cli.py              # CLI interface with Typer
│   └── publish_to_substack.py  # Core publishing logic
├── scripts/
│   └── export_notebook.py  # Notebook to markdown converter
├── docs/                    # Published content
├── templates/              # Jinja2 templates
├── archive/                # Archived documentation
├── Makefile               # Common tasks
└── requirements-substack.txt  # Python dependencies
```

## Dependencies

- **playwright**: Browser automation
- **playwright-stealth**: Anti-detection for browser automation
- **python-frontmatter**: Parse markdown front-matter
- **markdown-it-py**: Markdown to HTML conversion
- **typer**: CLI framework
- **rich**: Terminal formatting
- **nbformat**: Jupyter notebook handling
- **nbconvert**: Notebook conversion

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Type checking
mypy tools/ scripts/

# Linting
ruff check .

# Formatting
ruff format .
```

## Troubleshooting

### Login Issues

If login fails, try:
1. Delete `.playwright/storage_state.json`
2. Run `make substack-login` again
3. Check that your Substack subdomain is correct

### Publishing Errors

Debug artifacts are saved to `.playwright/`:
- `last_error.png` - Screenshot of failed state
- `last_error.html` - HTML of failed page

### Image Upload Issues

Images must be:
- Local files (not URLs)
- Relative paths from the markdown file
- In supported formats (PNG, JPG, GIF)

## License

MIT

## Contributing

Contributions welcome! Please:
1. Add tests for new features
2. Update documentation
3. Follow existing code style
4. Add type hints to all functions
