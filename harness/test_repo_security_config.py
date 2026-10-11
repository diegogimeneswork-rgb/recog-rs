"""Checks the repository's auditable GitHub security configuration."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
WORKFLOW = REPOSITORY / ".github/workflows/ci.yml"
DEPENDABOT = REPOSITORY / ".github/dependabot.yml"
SECURITY = REPOSITORY / "SECURITY.md"
SETTINGS = REPOSITORY / "docs/repository-security.md"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


class RepositorySecurityConfigTests(unittest.TestCase):
    def test_ci_is_read_only_for_pull_requests_and_pins_actions(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertRegex(workflow, r"(?m)^\s+pull_request:\s*$")
        self.assertNotIn("pull_request_target", workflow)
        self.assertNotIn("secrets.", workflow)
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertNotRegex(workflow, r"(?m)^\s*[a-z_-]+:\s*(write|read-all|write-all)\s*$")
        self.assertIn("persist-credentials: false", workflow)

        action_refs = re.findall(r"(?m)^\s*uses:\s*([^\s#]+)\s*$", workflow)
        self.assertTrue(action_refs, "CI must use at least one action")
        for action_ref in action_refs:
            self.assertIn("@", action_ref)
            self.assertRegex(action_ref.rsplit("@", 1)[1], FULL_SHA)

    def test_dependabot_updates_cargo_and_github_actions(self) -> None:
        config = DEPENDABOT.read_text(encoding="utf-8")
        for ecosystem in ("cargo", "github-actions"):
            with self.subTest(ecosystem=ecosystem):
                self.assertIn(f'package-ecosystem: "{ecosystem}"', config)
                self.assertRegex(
                    config,
                    rf'(?s)package-ecosystem: "{re.escape(ecosystem)}".*?directory: "/".*?interval: "weekly"',
                )

    def test_security_policy_describes_private_reporting(self) -> None:
        policy = SECURITY.read_text(encoding="utf-8").lower()
        self.assertIn("private vulnerability reporting", policy)
        self.assertIn("public issue", policy)

    def test_repository_settings_runbook_covers_remote_controls(self) -> None:
        guide = SETTINGS.read_text(encoding="utf-8").lower()
        for control in (
            "branch `main`",
            "require a pull request",
            "status check `verify`",
            "block force pushes",
            "read-only",
            "full commit sha",
            "dependabot alerts",
            "secret scanning",
            "push protection",
            "private vulnerability reporting",
        ):
            with self.subTest(control=control):
                self.assertIn(control, guide)


if __name__ == "__main__":
    unittest.main()
