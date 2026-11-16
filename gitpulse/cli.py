"""
GitPulse CLI Interface
"""
import argparse
import json
import sys
from .analyzer import GitPulseAnalyzer
from .scanner import scan_repository_for_secrets

def main():
    parser = argparse.ArgumentParser(
        prog="gitpulse",
        description="GitPulse: Developer Productivity Analytics & Secret Leak Scanner"
    )
    parser.add_argument("--path", default=".", help="Target repository directory (default: current directory)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: summary
    subparsers.add_parser("summary", help="Analyze repository velocity, commits, and author contributions")

    # Subcommand: changelog
    subparsers.add_parser("changelog", help="Generate changelog categorized by Conventional Commits")

    # Subcommand: scan
    subparsers.add_parser("scan", help="Scan repository for leaked credentials and API secrets")

    args = parser.parse_args()

    if not args.command or args.command == "summary":
        analyzer = GitPulseAnalyzer(args.path)
        summary = analyzer.get_summary()
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print("\n📊 --- GitPulse Repository Summary ---")
            print(f"Total Commits: {summary.get('total_commits', 0)}")
            print(f"Unique Contributors: {summary.get('unique_contributors', 0)}")
            print("\nTop Contributors:")
            for c in summary.get("top_contributors", []):
                print(f"  • {c['author']}: {c['commits']} commits ({c['percentage']}%)")
            print("--------------------------------------\n")

    elif args.command == "changelog":
        analyzer = GitPulseAnalyzer(args.path)
        changelog = analyzer.generate_changelog()
        if args.json:
            print(json.dumps(changelog, indent=2))
        else:
            print("\n📝 --- Conventional Changelog ---")
            for cat, items in changelog.items():
                print(f"\n### {cat}")
                for item in items:
                    print(f"  - {item}")
            print("\n---------------------------------\n")

    elif args.command == "scan":
        findings = scan_repository_for_secrets(args.path)
        if args.json:
            print(json.dumps(findings, indent=2))
        else:
            print("\n🔍 --- Security Secret Leak Scan ---")
            if not findings:
                print("✅ Clean: Zero exposed secrets detected.")
            else:
                print(f"⚠️ Warning: Found {len(findings)} potential leaked secrets:")
                for f in findings:
                    print(f"  [!] {f['rule']} in {f['file']}:{f['line']}")
            print("------------------------------------\n")

if __name__ == "__main__":
    main()
