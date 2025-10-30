# tools/substack/cli.py
import os
import re
import subprocess
import sys
from pathlib import Path

import typer
from rich import print as rprint

app = typer.Typer(help="NWSL Notes utilities for Substack")

# --- .env loading with inline-comment handling ---
ENV_LINE = re.compile(r"""^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$""")

def _strip_inline_comment(s: str) -> str:
    if "#" in s:
        s = s.split("#", 1)[0]
    return s.strip().strip('"').strip("'").strip()

def load_env() -> None:
    """Load environment variables from .env file."""
    env_path = Path(".env")
    if not env_path.exists():
        return
    for raw in env_path.read_text().splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        m = ENV_LINE.match(s)
        if not m:
            continue
        k, v = m.group(1), _strip_inline_comment(m.group(2))
        if v != "" and k not in os.environ:
            os.environ[k] = v

# --- subdomain normalization/validation ---
SUBSTACK_RE = re.compile(r"^[a-z0-9-]+$")

def normalize_space(space: str | None) -> str:
    """Normalize and validate a Substack subdomain.

    Args:
        space: Raw subdomain input

    Returns:
        Normalized subdomain string

    Raises:
        typer.BadParameter: If subdomain is invalid
    """
    if not space:
        return ""
    s = space.strip().strip('"').strip("'")
    if " " in s or "\t" in s:
        s = s.split()[0]
    s = s.lower()
    if not SUBSTACK_RE.match(s):
        raise typer.BadParameter(
            f"Invalid Substack subdomain: {space!r}. Use the part before .substack.com, e.g., 'nwsldata'."
        )
    return s

# --- commands ---
@app.command(help="Interactive login to capture a Substack session (storage_state.json).")
def login(space: str | None = typer.Option(None, "--space", "-s", help="Substack subdomain, e.g., nwsldata")) -> None:
    load_env()
    space = normalize_space(space or os.getenv("SUBSTACK_SPACE"))
    if not space:
        rprint("[red]Set SUBSTACK_SPACE in .env or pass --space[/red]")
        raise typer.Exit(1)
    pub = Path(__file__).parent / "publish_to_substack.py"
    cmd = [sys.executable, str(pub), "--space", space, "--login"]
    rprint(f"[cyan]Running:[/cyan] {' '.join(cmd)}")
    subprocess.check_call(cmd)

@app.command(help="Publish a Markdown file as a Substack draft (or live with --publish).")
def publish(
    path: Path = typer.Argument(..., help="Path to the Markdown file"),
    space: str | None = typer.Option(None, "--space", "-s", help="Substack subdomain, e.g., nwsldata"),
    live: bool = typer.Option(False, "--publish", help="Publish live (default: create/update draft)"),
) -> None:
    load_env()
    space = normalize_space(space or os.getenv("SUBSTACK_SPACE"))
    if not space:
        rprint("[red]Set SUBSTACK_SPACE in .env or pass --space[/red]")
        raise typer.Exit(1)
    if not path.exists():
        rprint(f"[red]File not found:[/red] {path}")
        raise typer.Exit(1)
    pub = Path(__file__).parent / "publish_to_substack.py"
    cmd = [sys.executable, str(pub), "--space", space, "--file", str(path)]
    if live is True:
        cmd.append("--publish")
    rprint(f"[cyan]Running:[/cyan] {' '.join(cmd)}")
    subprocess.check_call(cmd)

if __name__ == "__main__":
    app()
