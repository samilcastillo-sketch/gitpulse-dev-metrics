"""
DevSecOps Secret & Credential Leak Scanner
Detects inadvertently committed sensitive API keys and secrets.
"""
import re
import os
from typing import List, Dict

SECRET_PATTERNS = [
    ("AWS Access Key ID", re.compile(r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}")),
    ("GitHub Personal Access Token", re.compile(r"ghp_[0-9a-zA-Z]{36}")),
    ("Stripe API Secret", re.compile(r"sk_live_[0-9a-zA-Z]{24}")),
    ("Slack Bot Token", re.compile(r"xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}")),
    ("Private Key Header", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"))
]

IGNORED_DIRS = {".git", "node_modules", ".venv", "__pycache__"}

def scan_repository_for_secrets(base_path: str = ".") -> List[Dict[str, str]]:
    findings = []

    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            file_path = os.path.join(root, f)
            rel_path = os.path.relpath(file_path, base_path)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
                    for line_num, line in enumerate(fh, start=1):
                        for name, pattern in SECRET_PATTERNS:
                            if pattern.search(line):
                                findings.append({
                                    "rule": name,
                                    "file": rel_path,
                                    "line": line_num
                                })
            except Exception:
                continue

    return findings
