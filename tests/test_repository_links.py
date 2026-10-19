"""Validate file links and indexes without making network requests."""

from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def local_links(path):
    content = re.sub(r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", path.read_text(encoding="utf-8"),
                     flags=re.MULTILINE | re.DOTALL)
    for target in re.findall(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)", content):
        url = urlsplit(target.strip("<>"))
        if not url.scheme and not url.netloc and url.path:
            yield (path.parent / unquote(url.path)).resolve()


class RepositoryLinkTests(unittest.TestCase):
    def test_relative_file_links_exist(self):
        files = [ROOT / "README.md"]
        for folder in ("notes", "projects", "scripts"):
            files.extend((ROOT / folder).rglob("*.md"))
        for source in files:
            for target in local_links(source):
                with self.subTest(source=str(source.relative_to(ROOT)), target=str(target)):
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.exists(), "Linked path does not exist")

    def test_main_index_covers_all_notes_and_projects(self):
        indexed = set(local_links(ROOT / "README.md"))
        paths = list((ROOT / "notes").glob("*.md")) + list((ROOT / "projects").rglob("README.md"))
        for path in paths:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIn(path, indexed)

    def test_script_guide_covers_all_utilities(self):
        indexed = set(local_links(ROOT / "scripts" / "README.md"))
        for path in (ROOT / "scripts").glob("*.py"):
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIn(path, indexed)


if __name__ == "__main__":
    unittest.main()
