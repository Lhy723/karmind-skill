from __future__ import annotations

import subprocess
import sys
import unittest
import json
import importlib.util
import os
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]


class ScriptTests(unittest.TestCase):
    def run_cmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_init_wiki_creates_required_files(self) -> None:
        with TemporaryDirectory() as tmp:
            wiki = Path(tmp) / "demo"
            result = self.run_cmd("scripts/init_wiki.py", str(wiki))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((wiki / "AGENTS.md").exists())
            self.assertTrue((wiki / "raw").is_dir())
            self.assertTrue((wiki / "wiki" / "index.md").exists())
            self.assertTrue((wiki / "wiki" / "log.md").exists())
            self.assertTrue((wiki / "wiki" / "cache" / "ingest-cache.json").exists())
            self.assertTrue((wiki / "wiki" / "reports").is_dir())

    def test_skill_frontmatter_is_cli_friendly(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        header = skill.split("---", 2)[1]
        self.assertIn('name: "karmind-skill"', header)
        self.assertRegex(header, r'description:\s+"[^"]+"')

    def test_claude_plugin_distribution_is_valid(self) -> None:
        build = self.run_cmd("scripts/build_claude_plugin.py")
        self.assertEqual(build.returncode, 0, build.stderr)

        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        plugin = json.loads((ROOT / "plugins" / "karmind-skill" / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(marketplace["plugins"][0]["name"], "karmind-skill")
        self.assertEqual(plugin["name"], "karmind-skill")
        self.assertEqual(marketplace["plugins"][0]["source"], "./plugins/karmind-skill")

        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        plugin_skill = (ROOT / "plugins" / "karmind-skill" / "skills" / "karmind-skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(plugin_skill, root_skill)
        self.assertTrue((ROOT / "plugins" / "karmind-skill" / "skills" / "karmind-skill" / "scripts" / "init_wiki.py").exists())

    def test_init_wiki_can_import_existing_documents(self) -> None:
        with TemporaryDirectory() as tmp:
            wiki = Path(tmp) / "demo"
            wiki.mkdir()
            note = wiki / "notes.md"
            note.write_text("# Existing Notes\n", encoding="utf-8")

            result = self.run_cmd("scripts/init_wiki.py", str(wiki), "--import-existing", "move")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(note.exists())
            self.assertTrue((wiki / "raw" / "imported" / "notes.md").exists())

            cache_list = self.run_cmd("scripts/ingest_cache.py", str(wiki), "list", "--status", "pending")
            self.assertEqual(cache_list.returncode, 0, cache_list.stderr)
            self.assertIn("raw/imported/notes.md", cache_list.stdout)

    def test_wiki_doctor_reports_fresh_wiki(self) -> None:
        with TemporaryDirectory() as tmp:
            wiki = Path(tmp) / "demo"
            init = self.run_cmd("scripts/init_wiki.py", str(wiki))
            self.assertEqual(init.returncode, 0, init.stderr)

            doctor = self.run_cmd("scripts/wiki_doctor.py", str(wiki))
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            report = (wiki / "wiki" / "reports" / "doctor-report.md")
            self.assertTrue(report.exists())
            report_text = report.read_text(encoding="utf-8")
            self.assertIn("Broken links: 0", report_text)
            self.assertIn("Orphan pages:", report_text)
            self.assertIn("Cached pending raw files:", report_text)

    def test_ingest_cache_marks_processed(self) -> None:
        with TemporaryDirectory() as tmp:
            wiki = Path(tmp) / "demo"
            init = self.run_cmd("scripts/init_wiki.py", str(wiki))
            self.assertEqual(init.returncode, 0, init.stderr)
            raw_file = wiki / "raw" / "source.md"
            raw_file.write_text("# Source\n", encoding="utf-8")

            ensure = self.run_cmd("scripts/ingest_cache.py", str(wiki), "ensure")
            self.assertEqual(ensure.returncode, 0, ensure.stderr)
            mark = self.run_cmd(
                "scripts/ingest_cache.py",
                str(wiki),
                "mark",
                "raw/source.md",
                "--processor",
                "manual-agent",
                "--source-note",
                "wiki/sources/source.md",
                "--page",
                "wiki/concepts/source.md",
            )
            self.assertEqual(mark.returncode, 0, mark.stderr)
            listing = self.run_cmd("scripts/ingest_cache.py", str(wiki), "list", "--status", "processed")
            self.assertEqual(listing.returncode, 0, listing.stderr)
            self.assertIn("processed\traw/source.md", listing.stdout)

    def test_model_batch_ingest_dry_run_lists_pending(self) -> None:
        with TemporaryDirectory() as tmp:
            wiki = Path(tmp) / "demo"
            init = self.run_cmd("scripts/init_wiki.py", str(wiki))
            self.assertEqual(init.returncode, 0, init.stderr)
            raw_file = wiki / "raw" / "source.md"
            raw_file.write_text("# Source\n", encoding="utf-8")

            result = self.run_cmd("scripts/model_batch_ingest.py", str(wiki), "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("raw/source.md", result.stdout)

    def test_model_batch_ingest_loads_local_env(self) -> None:
        module_path = ROOT / "scripts" / "model_batch_ingest.py"
        spec = importlib.util.spec_from_file_location("model_batch_ingest", module_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.path.insert(0, str(ROOT / "scripts"))
        spec.loader.exec_module(module)

        old_values = {key: os.environ.get(key) for key in ["LLM_API_KEY", "LLM_MODEL", "LLM_BASE_URL"]}
        for key in old_values:
            os.environ.pop(key, None)
        try:
            with TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / ".env.local").write_text(
                    "LLM_API_KEY=test-key\nLLM_MODEL=test-model\nLLM_BASE_URL=https://example.test/v1\n",
                    encoding="utf-8",
                )
                module.load_local_env(root)
                self.assertEqual(os.environ.get("LLM_API_KEY"), "test-key")
                self.assertEqual(os.environ.get("LLM_MODEL"), "test-model")
                self.assertEqual(os.environ.get("LLM_BASE_URL"), "https://example.test/v1")
        finally:
            for key, value in old_values.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_install_lists_targets(self) -> None:
        result = self.run_cmd("scripts/install.py", "--list-targets")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("codex-user", result.stdout)
        self.assertIn("claude-user", result.stdout)
        self.assertIn("opencode-user", result.stdout)
        self.assertIn("project-trae also writes", result.stdout)

    def test_project_trae_installs_skill_and_rules(self) -> None:
        with TemporaryDirectory() as tmp:
            project = Path(tmp) / "wiki"
            project.mkdir()
            result = self.run_cmd("scripts/install.py", "--target", "project-trae", "--project", str(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / ".trae" / "skills" / "karmind-skill" / "SKILL.md").exists())
            self.assertTrue((project / ".trae" / "rules" / "project_rules.md").exists())


if __name__ == "__main__":
    unittest.main()
