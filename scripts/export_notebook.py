"""
Export a Jupyter notebook to Markdown with YAML front-matter.
Usage:
  python scripts/export_notebook.py --in nb.ipynb --out docs/nb.md --title "My Post" --tags eval,model-card
"""
import argparse
from pathlib import Path

import nbformat
from nbconvert import MarkdownExporter

FRONT = """---
title: "{title}"
tags: [{tags}]
---
"""

def main() -> None:
    """Export a Jupyter notebook to markdown with front-matter."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_nb", required=True)
    ap.add_argument("--out", dest="out_md", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--tags", default="")
    args = ap.parse_args()

    nb = nbformat.read(args.in_nb, as_version=4)
    exporter = MarkdownExporter()
    body, resources = exporter.from_notebook_node(nb)

    out = Path(args.out_md)
    out.parent.mkdir(parents=True, exist_ok=True)
    fm = FRONT.format(title=args.title.replace('"','\\"'),
                      tags=", ".join(t.strip() for t in args.tags.split(",") if t.strip()))
    out.write_text(fm + "\n" + body)
    print("Wrote", out)

if __name__ == "__main__":
    main()
