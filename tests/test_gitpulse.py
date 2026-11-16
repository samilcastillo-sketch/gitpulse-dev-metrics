"""
Automated Test Suite for GitPulse
"""
import unittest
import tempfile
import os
import shutil
import subprocess
from gitpulse.analyzer import GitPulseAnalyzer
from gitpulse.scanner import scan_repository_for_secrets

class TestGitPulse(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Initialize a test git repository
        subprocess.run(["git", "init"], cwd=self.test_dir, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=self.test_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.test_dir, check=True)

        # Create sample commit with conventional commit format
        readme = os.path.join(self.test_dir, "README.md")
        with open(readme, "w") as f:
            f.write("# Sample Project\n")
        subprocess.run(["git", "add", "."], cwd=self.test_dir, check=True)
        subprocess.run(["git", "commit", "-m", "feat: initial feature commit"], cwd=self.test_dir, check=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_analyzer_summary(self):
        analyzer = GitPulseAnalyzer(self.test_dir)
        summary = analyzer.get_summary()
        self.assertEqual(summary["total_commits"], 1)
        self.assertEqual(summary["unique_contributors"], 1)
        self.assertEqual(summary["top_contributors"][0]["author"], "Tester <test@example.com>")

    def test_analyzer_changelog(self):
        analyzer = GitPulseAnalyzer(self.test_dir)
        changelog = analyzer.generate_changelog()
        self.assertIn("Features", changelog)
        self.assertEqual(changelog["Features"][0], "feat: initial feature commit")

    def test_scanner_detects_credentials(self):
        # Create a file containing a simulated AWS key
        leaked_file = os.path.join(self.test_dir, "config.py")
        with open(leaked_file, "w") as f:
            f.write('AWS_KEY = "AKIAIOSFODNN7EXAMPLE"\n')

        findings = scan_repository_for_secrets(self.test_dir)
        self.assertTrue(len(findings) >= 1)
        self.assertEqual(findings[0]["rule"], "AWS Access Key ID")

if __name__ == "__main__":
    unittest.main()
