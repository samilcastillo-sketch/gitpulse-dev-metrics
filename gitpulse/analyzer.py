"""
GitPulse Analyzer Core
Extracts developer productivity metrics, commit patterns, and changelogs from Git repositories.
"""
import subprocess
from collections import defaultdict
from typing import Dict, List, Any

class GitPulseAnalyzer:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def _run_git(self, args: List[str]) -> str:
        res = subprocess.run(
            ["git", "-C", self.repo_path] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()

    def get_summary(self) -> Dict[str, Any]:
        """Calculates total commits, contributors, branches, and active authors."""
        try:
            total_commits = int(self._run_git(["rev-list", "--count", "HEAD"]))
        except Exception:
            return {"error": "Not a git repository or no commits found."}

        # Author distribution
        author_raw = self._run_git(["log", "--format=%an <%ae>"])
        authors = defaultdict(int)
        for line in author_raw.splitlines():
            if line:
                authors[line] += 1

        top_contributors = sorted(
            [{"author": k, "commits": v, "percentage": round((v / total_commits) * 100, 1)} for k, v in authors.items()],
            key=lambda x: x["commits"],
            reverse=True
        )

        return {
            "total_commits": total_commits,
            "unique_contributors": len(authors),
            "top_contributors": top_contributors[:5]
        }

    def generate_changelog(self, max_commits: int = 50) -> Dict[str, List[str]]:
        """Parses Conventional Commits format into structured categories."""
        log_raw = self._run_git(["log", f"-n{max_commits}", "--format=%s"])
        categories = {
            "Features": [],
            "Bug Fixes": [],
            "Refactoring": [],
            "Performance": [],
            "Documentation": [],
            "Other": []
        }

        for msg in log_raw.splitlines():
            msg = msg.strip()
            if not msg:
                continue
            if msg.startswith("feat:") or msg.startswith("feat("):
                categories["Features"].append(msg)
            elif msg.startswith("fix:") or msg.startswith("fix("):
                categories["Bug Fixes"].append(msg)
            elif msg.startswith("refactor:") or msg.startswith("refactor("):
                categories["Refactoring"].append(msg)
            elif msg.startswith("perf:") or msg.startswith("perf("):
                categories["Performance"].append(msg)
            elif msg.startswith("docs:") or msg.startswith("docs("):
                categories["Documentation"].append(msg)
            else:
                categories["Other"].append(msg)

        return {k: v for k, v in categories.items() if v}
