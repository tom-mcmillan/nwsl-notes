"""Pytest configuration and shared fixtures."""
from pathlib import Path

import pytest


@pytest.fixture
def sample_markdown(tmp_path: Path) -> Path:
    """Create a sample markdown file with frontmatter.

    Args:
        tmp_path: Pytest temporary directory

    Returns:
        Path to created markdown file
    """
    md_file = tmp_path / "sample.md"
    content = """---
title: "Sample Post"
tags: [test, sample]
---

# Sample Content

This is a test post with some **markdown**.

![Test Image](./images/test.png)
"""
    md_file.write_text(content)
    return md_file


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Create a sample image file.

    Args:
        tmp_path: Pytest temporary directory

    Returns:
        Path to created image file
    """
    img_dir = tmp_path / "images"
    img_dir.mkdir()
    img_file = img_dir / "test.png"
    # Create a minimal 1x1 PNG
    img_file.write_bytes(
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
        b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    return img_file
