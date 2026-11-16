# GitPulse: Developer Analytics & Secret Leak Scanner

Lightweight, high-performance CLI utility to analyze Git commit velocity, author contributions, conventional changelogs, and detect leaked secrets before pushing to production.

## Features

- **Commit Velocity & Author Breakdown:** Computes total commits, active authors, and contribution percentages across repositories.
- **Conventional Changelog Generator:** Categorizes commit logs automatically into Features, Bug Fixes, Refactoring, and Performance improvements.
- **DevSecOps Secret Scanner:** Scans local trees for committed credentials (AWS Keys, Stripe Secrets, GitHub PATs, and SSH/RSA Private Keys).
- **Zero Third-Party Dependencies:** Built entirely with the Python Standard Library.

## Usage

```bash
# Display repository metrics summary
python3 -m gitpulse.cli summary

# Generate formatted changelog
python3 -m gitpulse.cli changelog

# Scan repository for exposed secrets
python3 -m gitpulse.cli scan

# Output results in structured JSON format
python3 -m gitpulse.cli summary --json
```

## Running Automated Tests

```bash
python3 -m unittest discover tests -v
```
