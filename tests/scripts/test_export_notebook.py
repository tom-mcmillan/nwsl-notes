"""Tests for export_notebook module."""

import pytest


class TestExportNotebook:
    """Tests for notebook export functionality."""

    def test_export_basic_notebook(self, tmp_path):
        """Test exporting a basic notebook."""
        pytest.skip("Requires test notebook fixture")

    def test_export_with_frontmatter(self, tmp_path):
        """Test that frontmatter is correctly added."""
        pytest.skip("Requires test notebook fixture")

    def test_export_nonexistent_notebook(self, tmp_path):
        """Test that exporting nonexistent notebook fails gracefully."""
        pytest.skip("Requires implementation")
