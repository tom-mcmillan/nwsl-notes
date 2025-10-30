# AI-Powered Substack Publishing Workflow

This guide explains how to use AI agents to write and publish Substack posts for nwsldata.

## Quick Start

### 1. Start a Writing Session

Tell your AI agent:
```
I want to write a Substack post about [TOPIC].
Please read the instructions in .claude/prompts/substack-writer.md
and write a post following that format.
```

### 2. Review the Generated Post

The agent should create a file in `docs/` like:
```
docs/2024-10-28-your-topic-name.md
```

Check that it has:
- ✅ YAML frontmatter at the top
- ✅ Title and tags in frontmatter
- ✅ Proper markdown formatting
- ✅ Clear structure with headers
- ✅ Engaging content

### 3. Publish to Substack

```bash
# Publish as draft (recommended first time)
make substack-publish FILE=docs/2024-10-28-your-topic-name.md

# Review draft on Substack website
# If looks good, publish live:
make substack-publish FILE=docs/2024-10-28-your-topic-name.md PUBLISH=true
```

## Detailed Workflow

### Option A: New Post from Scratch

```
User: "Write a Substack post analyzing the top goal scorers in NWSL 2024.
       Use the prompt in .claude/prompts/substack-writer.md"

Agent: [Reads prompt, writes post with proper frontmatter]

User: "Save it to docs/2024-10-28-top-scorers-analysis.md"

Agent: [Saves file]

User: "Great! Now publish as draft"

Agent: [Runs make command to publish draft]
```

### Option B: Post from Jupyter Notebook

If you have a data analysis notebook:

```bash
# First, export notebook to markdown
make nb2md \
  NB=analysis/goal-scoring.ipynb \
  OUT=docs/2024-10-28-goal-scoring-analysis.md \
  TITLE="NWSL Goal Scoring Trends 2024" \
  TAGS="nwsl,analysis,stats,goals"

# Review and edit the markdown file
# Then publish
make substack-publish FILE=docs/2024-10-28-goal-scoring-analysis.md
```

### Option C: Interactive Writing with AI

```
User: "I want to write about tactical trends in NWSL.
       Read .claude/prompts/substack-writer.md for format guidelines."

Agent: "I've read the guidelines. What specific tactical aspect should I focus on?"

User: "Let's analyze pressing strategies across teams"

Agent: "Great! Should I include:
       - Specific teams to highlight?
       - Recent matches to reference?
       - Particular metrics (PPDA, press success rate)?"

User: [Provides context]

Agent: [Writes comprehensive post]
```

## Post Structure Template

Every post should follow this structure:

```markdown
---
title: "Compelling Title That Describes Content"
tags: [nwsl, category, subject, topic]
---

# Main Title (matches frontmatter title)

Hook paragraph that grabs attention...

## Introduction

Set the stage, explain what you'll cover...

## Main Analysis / Content

### Subsection 1

Content with data, analysis...

### Subsection 2

More detailed exploration...

## Key Takeaways / Conclusion

Summarize findings, implications...
```

## Content Ideas & Tag Combinations

### Player Analysis
```yaml
tags: [nwsl, analysis, players, stats]
```
- Individual player deep dives
- Position-specific analysis
- MVP/award races
- Breakout performers

### Team Analysis
```yaml
tags: [nwsl, teams, tactics, analysis]
```
- Team performance reviews
- Tactical breakdowns
- Formation analysis
- Team comparisons

### Match Coverage
```yaml
tags: [nwsl, recap, match, analysis]
```
- Match recaps with stats
- Preview articles
- Head-to-head comparisons

### Data Deep Dives
```yaml
tags: [nwsl, data, stats, visualization]
```
- League-wide statistical trends
- Historical comparisons
- Advanced metrics explanations
- Data visualization walkthroughs

### League News & Trends
```yaml
tags: [nwsl, news, trends, opinion]
```
- Rule changes impact
- Season predictions
- Transfer analysis
- League development

## AI Agent Context Checklist

When asking an AI to write a post, provide:

### Required Context
- [ ] Link to prompt: `.claude/prompts/substack-writer.md`
- [ ] Topic/angle for the post
- [ ] Target date for filename

### Optional but Helpful
- [ ] Specific data/stats to include
- [ ] Players/teams to focus on
- [ ] Tone preference (technical vs accessible)
- [ ] Target length (default: 500-1500 words)
- [ ] Related previous posts for consistency
- [ ] Available images/charts to reference

## Example AI Prompts

### Basic Post Request
```
Write a Substack post about [TOPIC]. Follow the format
in .claude/prompts/substack-writer.md and save to
docs/2024-10-28-[slug].md
```

### Detailed Post Request
```
I need a Substack post analyzing the NWSL playoff race.

Please:
1. Read .claude/prompts/substack-writer.md for format requirements
2. Focus on the top 4 teams
3. Include points, goal differential, and remaining schedule
4. Keep it accessible for casual fans
5. Use tags: [nwsl, playoffs, teams, analysis]
6. Save to docs/2024-10-28-playoff-race-analysis.md
```

### Data-Driven Post Request
```
Using the data in analysis/passing_stats.csv, write a
Substack post about passing patterns in NWSL.

Requirements:
- Follow .claude/prompts/substack-writer.md format
- Include top 3 teams by completion percentage
- Explain what the metrics mean (progressive passes, etc)
- Add a data table
- Tags: [nwsl, data, stats, tactics]
- Save to docs/2024-10-28-passing-analysis.md
```

## Publishing Checklist

Before publishing, verify:

- [ ] **Frontmatter present**: `---` at top and bottom
- [ ] **Title in frontmatter**: Matches main heading
- [ ] **Tags in frontmatter**: 2-5 relevant tags
- [ ] **Headers structured**: H1 for title, H2 for sections
- [ ] **Links work**: No broken references
- [ ] **Images referenced**: Paths correct (if using images)
- [ ] **Proofread**: No obvious typos or errors
- [ ] **Data accurate**: Stats and numbers verified
- [ ] **Filename correct**: `docs/YYYY-MM-DD-slug.md`

## Troubleshooting

### Post not formatting correctly on Substack?
- Check that frontmatter has `---` delimiters
- Ensure no special characters in title
- Verify markdown syntax (especially lists and tables)

### Images not uploading?
- Use relative paths: `../images/chart.png`
- Ensure images exist locally
- Supported formats: PNG, JPG, GIF

### Tags not appearing?
- Check YAML array format: `[tag1, tag2]`
- No quotes around individual tags
- Keep tags lowercase

### Draft vs Publish?
- **Always draft first** to review on Substack
- Check formatting, images, links
- Then publish with `PUBLISH=true`

## Tips for Better AI-Generated Posts

1. **Be specific**: "Analyze xG trends" vs "Write about goals"
2. **Provide data**: Link to CSV, stats, or paste data
3. **Set constraints**: Word count, sections, focus
4. **Reference examples**: "Like the post in docs/2024-09-15-..."
5. **Iterate**: Ask for revisions, additions, clarifications
6. **Review carefully**: AI is good but not perfect

## File Organization

```
docs/
├── 2024-10-28-mvp-race-analysis.md
├── 2024-10-25-tactical-trends.md
├── 2024-10-20-playoff-preview.md
└── images/
    ├── chart-goals.png
    └── heatmap-passes.png

.claude/prompts/
└── substack-writer.md  # Agent instructions

templates/posts/
└── example-post.md     # Reference template
```

## Advanced: Custom Slash Commands

You can create a custom slash command for quick post generation:

`.claude/commands/writepost.md`:
```markdown
Write a Substack post about the topic I specify.

1. Read the guidelines in .claude/prompts/substack-writer.md
2. Ask me for: topic, focus, specific data to include
3. Generate the post following the exact format
4. Save to docs/ with today's date in filename
5. Offer to publish as draft
```

Then use: `/writepost` in Claude Code

## Resources

- **Format Guide**: `.claude/prompts/substack-writer.md`
- **Example Post**: `templates/posts/example-post.md`
- **Main README**: `README.md`
- **Publishing Tools**: `tools/substack/`

## Questions?

If the AI agent produces incorrect format:
1. Re-share the prompt file
2. Show the example template
3. Explicitly state: "Must have YAML frontmatter"
4. Provide corrected example

The key is being explicit about requirements!
