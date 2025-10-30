import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

import frontmatter
from markdown_it import MarkdownIt
from playwright.async_api import Locator, Page, async_playwright
from playwright.async_api import TimeoutError as PWTimeout

try:
    from tools.substack.logger import setup_logger
except ImportError:
    from logger import setup_logger

logger = setup_logger(__name__)

SUBSTACK_RE = re.compile(r"^[a-z0-9-]+$")

def _normalize_space(space: str) -> str:
    """Normalize and validate Substack subdomain.

    Args:
        space: Raw subdomain string

    Returns:
        Normalized subdomain

    Raises:
        ValueError: If subdomain format is invalid
    """
    s = space.strip().strip('"').strip("'").split()[0].lower()
    if not SUBSTACK_RE.match(s):
        logger.error(f"Invalid Substack subdomain format: {space!r}")
        raise ValueError(f"Invalid Substack subdomain: {space!r}")
    return s

md = MarkdownIt("commonmark", {"breaks": True, "linkify": True}).enable("table")
IMG_RE = re.compile(r'!\[(?P<alt>[^\]]*)\]\((?P<fp>[^)]+)\)')

def find_local_images(markdown_text: str, base_dir: Path) -> list[Path]:
    """Find all local image paths referenced in markdown text.

    Args:
        markdown_text: The markdown content to search
        base_dir: Base directory for resolving relative paths

    Returns:
        List of Path objects for existing local images
    """
    assets: list[Path] = []
    for m in IMG_RE.finditer(markdown_text):
        fp = m.group("fp").split()[0].strip()
        if fp.startswith(("http://", "https://")):
            continue
        p = (base_dir / fp).resolve()
        if p.exists():
            assets.append(p)
    return assets

def read_post(md_path: Path) -> tuple[str, list[str], str, list[Path]]:
    """Read and parse a markdown post file.

    Args:
        md_path: Path to the markdown file

    Returns:
        Tuple of (title, tags, html_content, local_image_paths)

    Raises:
        FileNotFoundError: If markdown file doesn't exist
        ValueError: If file cannot be parsed
    """
    if not md_path.exists():
        logger.error(f"Markdown file not found: {md_path}")
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    try:
        post = frontmatter.load(md_path)
        title = post.get("title") or md_path.stem.replace("-", " ").title()
        tags = post.get("tags", [])
        html = md.render(post.content)
        html = html.replace('<code class="language-', '<code data-language="')
        assets = find_local_images(post.content, base_dir=md_path.parent)

        logger.info(f"Parsed post: {title} with {len(tags)} tags and {len(assets)} images")
        return title, tags, html, assets
    except Exception as e:
        logger.error(f"Failed to parse markdown file {md_path}: {e}")
        raise ValueError(f"Failed to parse markdown file: {e}") from e

async def _goto_any_editor(page: Page, space: str) -> None:
    """Try a few known 'new post' URLs until one loads the editor container.

    Args:
        page: Playwright page object
        space: Substack subdomain

    Raises:
        RuntimeError: If no editor URL succeeds
    """
    candidates = [
        f"https://{space}.substack.com/p/new",
        f"https://{space}.substack.com/publish/post/new",
        f"https://{space}.substack.com/write",
        f"https://{space}.substack.com/publish",
    ]
    last_err: Exception | None = None
    for url in candidates:
        try:
            logger.debug(f"Attempting to load editor at: {url}")
            await page.goto(url, wait_until="networkidle")
            # wait for *some* editor-ish element to appear
            await page.wait_for_timeout(500)
            if await _probe_editor_ready(page):
                logger.info(f"Successfully loaded editor at: {url}")
                return
        except PWTimeout as e:
            logger.warning(f"Timeout loading {url}: {e}")
            last_err = e
        except Exception as e:
            logger.warning(f"Error loading {url}: {e}")
            last_err = e
    # If we're here, none worked
    logger.error(f"Failed to load editor for space '{space}'")
    raise RuntimeError(f"Could not load Substack editor for space '{space}'. Last error: {last_err!r}")

async def _probe_editor_ready(page: Page) -> bool:
    """Return True if the editor seems present."""
    # Any of these being present suggests editor is mounted.
    probes = [
        '[data-testid="post-title"]',
        '[data-testid="post-body"]',
        'div[contenteditable="true"]',
        'textarea[placeholder*="Title"]',
        '[placeholder*="Title"]',
        '[role="textbox"]',
    ]
    for sel in probes:
        if await page.locator(sel).count():
            return True
    return False

async def _find_title_locator(page: Page) -> Locator | None:
    """Find a robust locator for the title field."""
    candidates = [
        '[data-testid="post-title"]',
        'textarea[placeholder*="Title"]',
        '[placeholder*="Title"]',
        # some editors use the first contenteditable as Title
        'div[contenteditable="true"] >> nth=0',
        # generic textbox (first)
        '[role="textbox"] >> nth=0',
    ]
    for sel in candidates:
        loc = page.locator(sel)
        if await loc.count():
            return loc.first
    return None

async def _find_body_locator(page: Page) -> Locator | None:
    """Find a robust locator for the body field."""
    candidates = [
        '[data-testid="post-body"]',
        # second contenteditable often is body
        'div[contenteditable="true"] >> nth=1',
        # fallback: last contenteditable
        'div[contenteditable="true"] >> nth=-1',
        # generic textbox (second)
        '[role="textbox"] >> nth=1',
    ]
    for sel in candidates:
        loc = page.locator(sel)
        if await loc.count():
            return loc.first
    return None

async def _dump_failure_artifacts(page: Page, note: str) -> None:
    """Save debugging artifacts (screenshot and HTML) on failure.

    Args:
        page: Playwright page object
        note: Description of the failure
    """
    outdir = Path(".playwright")
    outdir.mkdir(parents=True, exist_ok=True)
    png = outdir / "last_error.png"
    html = outdir / "last_error.html"
    try:
        await page.screenshot(path=str(png), full_page=True)
        html_text = await page.content()
        html.write_text(html_text, encoding="utf-8")
        logger.info(f"Debug artifacts saved: {png} and {html} ({note})")
        print(f">> Debug saved: {png} and {html}  ({note})")
    except Exception as e:
        logger.error(f"Failed to write debug artifacts: {e}")
        print(f">> Failed to write debug artifacts: {e}")

async def create_or_update_draft(
    space: str,
    md_file: Path | None,
    publish: bool,
    login: bool
) -> None:
    """Create or update a Substack draft or publish a post.

    Args:
        space: Substack subdomain (e.g., 'nwsldata')
        md_file: Path to markdown file to publish (required unless login=True)
        publish: If True, publish immediately; if False, save as draft
        login: If True, perform interactive login and save session
    """
    space = _normalize_space(space)
    storage_path = Path(".playwright") / "storage_state.json"
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True if not login else False)
        context = await browser.new_context(
            storage_state=None if login else (json.loads(storage_path.read_text()) if storage_path.exists() else None)
        )
        page = await context.new_page()

        # 1) Navigate to editor
        await _goto_any_editor(page, space)

        if login:
            print(">> Log in to Substack in the opened window, then return here and press Enter.")
            input()
            await context.storage_state(path=str(storage_path))
            print(">> Session saved:", storage_path)
            await browser.close()
            return

        if md_file is None:
            raise SystemExit("--file is required unless --login is provided")

        title, tags, html, assets = read_post(md_file)

        # 2) Find title/body locators robustly
        title_loc = await _find_title_locator(page)
        body_loc  = await _find_body_locator(page)
        if not title_loc or not body_loc:
            await _dump_failure_artifacts(page, "editor-not-found")
            raise SystemExit("Could not find the Substack editor fields. See .playwright/last_error.* for diagnostics.")

        # 3) Set title
        await title_loc.click()
        mod = "Meta" if sys.platform == "darwin" else "Control"
        await page.keyboard.press(f"{mod}+A")
        await page.keyboard.insert_text(title)

        # 4) Paste HTML into body (let Substack convert)
        await body_loc.click()
        await page.evaluate(f"navigator.clipboard.writeText({json.dumps(html)})")
        await page.keyboard.press(f"{mod}+V")
        await page.wait_for_timeout(900)

        # 5) Upload local images (best-effort)
        for img in assets:
            try:
                await page.keyboard.press("Enter")
                await page.keyboard.type("/image")
                await page.wait_for_timeout(350)
                image_menu = page.locator('role=menuitem[name*="Image"]')
                if await image_menu.count():
                    await image_menu.first.click()
                file_input = page.locator('input[type="file"]').first
                if await file_input.count():
                    await file_input.set_input_files(str(img))
                    await page.wait_for_timeout(900)
            except Exception:
                pass  # non-fatal

        # 6) Try to add tags if settings exists (non-fatal)
        try:
            settings = page.locator('[data-testid="post-settings"], [aria-label*="Settings"]')
            if await settings.count():
                await settings.first.click()
                tag_input = page.locator('input[placeholder*="Add tag"], input[aria-label*="tag"]')
                if await tag_input.count():
                    for t in tags:
                        await tag_input.fill(t)
                        await page.keyboard.press("Enter")
                # close modal
                try:
                    await page.keyboard.press("Escape")
                except Exception:
                    close_btn = page.locator('button:has-text("Close"), [aria-label*="Close"]')
                    if await close_btn.count():
                        await close_btn.first.click()
        except Exception:
            pass

        # 7) Save draft or publish
        if publish:
            # Try publish buttons
            publish_btn = page.locator('button:has-text("Publish"), [data-testid="publish-button"]')
            if await publish_btn.count():
                await publish_btn.first.click()
                confirm = page.locator('button:has-text("Publish now"), button:has-text("Publish")')
                if await confirm.count():
                    await confirm.first.click()
            else:
                await _dump_failure_artifacts(page, "publish-button-missing")
                raise SystemExit("Couldn't find Publish button. See .playwright/last_error.*")
        else:
            save = page.locator('button:has-text("Save draft"), [data-testid*="save-draft"]')
            if await save.count():
                await save.first.click()
            else:
                # sometimes autosave; try opening menu then saving
                menu = page.locator('button:has-text("Save"), [aria-label*="Save"]')
                if await menu.count():
                    await menu.first.click()
                else:
                    print(">> Draft may have auto-saved; continuing.")

        print(f">> {'Published' if publish else 'Draft saved'}: {md_file}")
        await context.storage_state(path=str(storage_path))
        await browser.close()

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--space", required=True, help="Substack subdomain (e.g., nwsldata)")
    ap.add_argument("--file", help="Markdown file path (required unless --login)")
    ap.add_argument("--publish", action="store_true", help="Publish instead of saving draft")
    ap.add_argument("--login", action="store_true", help="Interactive login to capture session")
    args = ap.parse_args()
    md_file = Path(args.file) if args.file else None
    asyncio.run(create_or_update_draft(args.space, md_file, args.publish, args.login))

if __name__ == "__main__":
    main()
