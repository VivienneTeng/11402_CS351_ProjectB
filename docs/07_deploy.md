# 07. Deployment Guide

This guide explains how to build and run the system from scratch on a developer machine, how to run tests, and a minimal CI suggestion.

## 1. Prerequisites
- Python 3.10 or later installed and on `PATH`.
- Git installed for cloning the repository.

## 2. Clone the repository

```bash
git clone https://github.com/your-username/11402_CS351_ProjectB.git
cd 11402_CS351_ProjectB
```

Replace `your-username` with the correct owner if different.

## 3. Create and activate a virtual environment

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

## 4. Install development dependencies

Create a `requirements-dev.txt` (if not present) with at least `pytest` and any CLI helpers. Then:

```bash
pip install -r requirements-dev.txt
```

If the project has a `pyproject.toml` / `requirements.txt`, install from those instead.

## 5. Project layout and entrypoint

Suggested entrypoint: `python -m app.main` or `python app/main.py` depending on project layout. Example run commands:

```bash
python -m app.main list
python -m app.main add --title "New Game" --platform PC --price 0
```

If your repository places the CLI entrypoint at `src/main.py`, use that path instead.

## 6. Initializing data directory

On first run the app will create `data/database.csv` automatically if missing. To initialize manually, run the provided storage init command (if implemented):

```bash
python -m app.main init
```

## 7. Running tests

Run unit and integration tests with `pytest`:

```bash
pytest -q
```

To run only acceptance tests:

```bash
pytest tests/acceptance -q
```

## 8. CI (GitHub Actions) snippet

Add a minimal workflow `.github/workflows/ci.yml` to run tests on push and PRs. Example:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python: [3.10]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python }}
      - name: Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate || .\.venv\Scripts\Activate.ps1
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest -q
```

Adjust activation commands per OS in the workflow if necessary.

## 9. Troubleshooting
- If Python reports modules missing, ensure the virtualenv is activated and `pip install -r requirements-dev.txt` completed successfully.
- If `data/database.csv` is corrupted, move it aside and restart the app to allow automatic re-initialization.

## 10. Next steps
- Add `requirements-dev.txt` and a small `Makefile` or PowerShell script to simplify common commands (`setup`, `test`, `clean`).

This guide gives users the commands needed to build and run the system from scratch and a minimal CI template to validate builds and tests.
