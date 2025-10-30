---
title: "NWSL Notes Smoke Test"
tags: [intro, test]
---

# docs.md Smoke Test ✅

This is a minimal smoke test post created from the CLI.

- Renders Markdown (headings, lists, emphasis)
- Contains a fenced code block
- Safe front-matter for title/tags

## Sample code

~~~python
print("Hello, Substack from docs.md!")
~~~

## Notes

- You can publish this as a draft with:
  - `make substack-publish FILE=docs/docs.md`
  - or `python tools/substack/cli.py publish docs/docs.md`
