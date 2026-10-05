"""Regression checks for upload blockers previously missed by package validation."""
from __future__ import annotations

import importlib.util
import json
import shutil
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preflight", ROOT / "scripts/openai_preflight.py")
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "package"
        self.root.mkdir()
        for name in ("plugin.json", "mcp.json"):
            shutil.copyfile(ROOT / name, self.root / name)
        for name in ("skills", "assets"):
            shutil.copytree(ROOT / name, self.root / name)

    def update_manifest(self, change):
        path = self.root / "plugin.json"
        manifest = json.loads(path.read_text())
        change(manifest)
        path.write_text(json.dumps(manifest))

    def archive(self, extra=None):
        path = Path(self.temp.name) / "package.zip"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            for file in self.root.rglob("*"):
                if file.is_file():
                    archive.write(file, file.relative_to(self.root).as_posix())
            if extra:
                extra(archive)
        return path

    def test_real_public_package_and_zip_pass_draft_checks(self):
        self.assertEqual(preflight.check_source(self.root), [])
        self.assertEqual(preflight.check_zip(self.archive()), [])

    def test_final_mode_requires_actual_video(self):
        self.assertTrue(any("demo_recording_url" in x for x in preflight.check_source(self.root, submission=True)))

    def test_country_omission_and_explicit_empty_are_valid(self):
        for value in (None, []):
            def change(manifest):
                publication = manifest["extensions"]["com.openai"]["publication"]
                if value is None:
                    publication.pop("countries", None)
                else:
                    publication["countries"] = value
            self.update_manifest(change)
            self.assertFalse(any("countries" in x for x in preflight.check_source(self.root)))

    def test_supplied_publication_countries_are_valid(self):
        self.update_manifest(lambda m: m["extensions"]["com.openai"]["publication"].update(countries=["US", "GB", "AU", "NZ"]))
        self.assertEqual(preflight.check_source(self.root), [])

    def test_semver_rejects_numeric_prerelease_leading_zero(self):
        self.update_manifest(lambda m: m.update(version="1.0.0-01"))
        self.assertTrue(any("semantic version" in x for x in preflight.check_source(self.root)))

    def test_public_support_file_symlink_cannot_leak_external_content(self):
        target = Path(self.temp.name) / "outside.txt"
        target.write_text("fixture")
        (self.root / "assets/leak.txt").symlink_to(target)
        self.assertTrue(any("regular file/directory" in x for x in preflight.check_source(self.root)))

    def test_fake_country_code_rejected(self):
        self.update_manifest(lambda m: m["extensions"]["com.openai"]["publication"].update(countries=["XX"]))
        self.assertTrue(any("countries" in x for x in preflight.check_source(self.root)))

    def test_unquoted_description_colon_is_not_valid_yaml(self):
        path = self.root / "skills/board-briefing/SKILL.md"
        path.write_text("---\nname: board-briefing\ndescription: Board briefing: executive results\n---\nInstructions.\n")
        self.assertTrue(any("board-briefing: invalid YAML" in x for x in preflight.check_source(self.root)))

    def test_whitespace_skill_and_duplicate_identity_rejected(self):
        path = self.root / "skills/board-briefing/SKILL.md"
        path.write_text("---\nname: anomaly-triage\ndescription: '  '\n---\nInstructions.\n")
        errors = preflight.check_source(self.root)
        self.assertTrue(any("invalid description" in x for x in errors))
        self.assertTrue(any("duplicate skill identity" in x for x in errors))

    def test_normalized_prompt_duplicates_rejected(self):
        self.update_manifest(lambda m: m["extensions"]["com.openai"]["interface"].update(defaultPrompt=["Read results", "Read   results"]))
        self.assertTrue(any("duplicates after" in x for x in preflight.check_source(self.root)))

    def test_invisible_and_whitespace_listing_rejected(self):
        self.update_manifest(lambda m: m["extensions"]["com.openai"]["interface"].update(displayName="  ", shortDescription="Read\u200b results"))
        errors = preflight.check_source(self.root)
        self.assertTrue(any("displayName" in x for x in errors))
        self.assertTrue(any("shortDescription" in x for x in errors))

    def test_embedded_credentials_and_missing_host_rejected(self):
        self.assertFalse(preflight.https_ok("https://user:password@lifesight.io"))
        self.assertFalse(preflight.https_ok("https:///missing-host"))

    def test_hook_and_reviewer_secrets_not_public_metadata(self):
        self.update_manifest(lambda m: m["extensions"]["com.openai"].update(hooks={}, review={"test_credentials": "fixture"}))
        errors = preflight.check_source(self.root)
        self.assertTrue(any("lifecycle hooks" in x for x in errors))
        self.assertTrue(any("secure portal" in x for x in errors))

    def test_optional_dark_asset_and_traversal_checked(self):
        self.update_manifest(lambda m: m["extensions"]["com.openai"]["interface"].update(logoDark="./../outside.svg"))
        self.assertTrue(any("logoDark" in x for x in preflight.check_source(self.root)))

    def test_malformed_svg_rejected(self):
        (self.root / "assets/icon.svg").write_text('<svg viewBox="0 0 100 100"><broken>')
        self.assertTrue(any("malformed XML" in x for x in preflight.check_source(self.root)))

    def test_zip_traversal_rejected(self):
        path = self.archive(lambda z: z.writestr("../outside.txt", "fixture"))
        self.assertTrue(any("unsafe archive path" in x for x in preflight.check_zip(path)))

    def test_zip_normalization_collision_rejected(self):
        path = self.archive(lambda z: z.writestr("ASSETS/icon.svg", "fixture"))
        self.assertTrue(any("normalized collision" in x for x in preflight.check_zip(path)))

    def test_zip_symlink_rejected(self):
        def extra(archive):
            info = zipfile.ZipInfo("assets/link.svg")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(info, "../../outside")
        self.assertTrue(any("unsupported/encrypted" in x for x in preflight.check_zip(self.archive(extra))))

    def test_zip_payload_revalidated_not_just_source(self):
        (self.root / "skills/board-briefing/SKILL.md").write_text("---\nname: board\ndescription: Broken: YAML\n---\nInstructions.")
        self.assertTrue(any("invalid YAML" in x for x in preflight.check_zip(self.archive())))


if __name__ == "__main__":
    unittest.main()
