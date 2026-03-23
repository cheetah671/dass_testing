# DASS Testing Project

This repository contains three testing parts:

1. `blackbox/` - Black-box API testing (QuickCart)
2. `integration/` - Integration testing (StreetRace Manager)
3. `whitebox/` - White-box testing (MoneyPoly)

---

## 1. Project Structure

```text
dass_testing/
	README.md
	blackbox/
		tests/
		report.pdf
	integration/
		code/
		tests/
		diagrams/
		report.pdf
	whitebox/
		moneypoly/
		tests/
		diagrams/
		report.pdf
```

---

## 2. Prerequisites

- Python 3.10+ (recommended: conda env `autograder`)
- `pytest`
- `requests` (used by black-box tests)
- Docker (required only for QuickCart server in black-box part)

Optional but recommended:

- Activate your conda environment before running tests:

```bash
conda activate autograder
```

---

## 3. Black-Box Part (`blackbox/`)

### 3.1 What it tests

- External API behavior of QuickCart using request/response validation.
- No internal implementation assumptions.

### 3.2 Start QuickCart server

From repo root:

```bash
cd blackbox
docker load -i quickcart_image_x86.tar
docker run -p 8080:8080 quickcart
```

If your image tag differs, use the loaded image name shown by Docker.

### 3.3 Run black-box tests

From repo root in a new terminal:

```bash
conda activate autograder
cd /home/arnav-agnihotri/Downloads/dass_testing/dass_testing
QC_BASE_URL=http://localhost:8080 QC_ROLL_NUMBER=2024101103 python -m pytest blackbox/tests/test_quickcart_api.py -q
```

Verbose run:

```bash
QC_BASE_URL=http://localhost:8080 QC_ROLL_NUMBER=2024101103 python -m pytest blackbox/tests/test_quickcart_api.py -vv
```

---

## 4. Integration Part (`integration/`)

### 4.1 What it tests

- Module-to-module behavior of StreetRace Manager:
	- registration, crew, inventory, races, results, missions, garage, reputation.

### 4.2 Run StreetRace Manager app

From repo root:

```bash
conda activate autograder
python integration/code/main.py
```

### 4.3 Run integration tests

From repo root:

```bash
conda activate autograder
pytest integration/tests -q
```

Run a specific integration test file:

```bash
pytest integration/tests/test_streetrace_integration.py -q
```

---

## 5. White-Box Part (`whitebox/`)

### 5.1 What it tests

- Internal decision paths and branch logic of MoneyPoly.
- Includes focused unit tests and deeper decision-path/integration-style tests.

### 5.2 Run MoneyPoly app

From repo root:

```bash
conda activate autograder
python whitebox/moneypoly/moneypoly/main.py
```

Alternative (run from package folder):

```bash
conda activate autograder
cd whitebox/moneypoly/moneypoly
python main.py
```

### 5.3 Run white-box tests

From repo root:

```bash
conda activate autograder
pytest whitebox/tests -q
```

Run a specific file:

```bash
pytest whitebox/tests/test_ui_paths.py -q
```

Collect tests only:

```bash
pytest whitebox/tests --collect-only -q
```

### 5.4 Run `pylint` for Whitebox (per file)

From repo root:

```bash
conda activate autograder

# Entry point
pylint whitebox/moneypoly/moneypoly/main.py

# Package modules
pylint whitebox/moneypoly/moneypoly/moneypoly/bank.py
pylint whitebox/moneypoly/moneypoly/moneypoly/board.py
pylint whitebox/moneypoly/moneypoly/moneypoly/cards.py
pylint whitebox/moneypoly/moneypoly/moneypoly/config.py
pylint whitebox/moneypoly/moneypoly/moneypoly/dice.py
pylint whitebox/moneypoly/moneypoly/moneypoly/game.py
pylint whitebox/moneypoly/moneypoly/moneypoly/player.py
pylint whitebox/moneypoly/moneypoly/moneypoly/property.py
pylint whitebox/moneypoly/moneypoly/moneypoly/ui.py
```

Run all Whitebox code files in one command:

```bash
conda activate autograder
pylint whitebox/moneypoly/moneypoly/main.py whitebox/moneypoly/moneypoly/moneypoly/*.py
```

### 5.5 Run Whitebox Code Files Directly (debug/manual checks)

From repo root:

```bash
conda activate autograder

# Main runnable app
python whitebox/moneypoly/moneypoly/main.py

# If needed, run a specific module file directly
python whitebox/moneypoly/moneypoly/moneypoly/game.py
python whitebox/moneypoly/moneypoly/moneypoly/player.py
python whitebox/moneypoly/moneypoly/moneypoly/bank.py
```

Note: Main gameplay should be started via `main.py`; module file execution is mainly for quick debugging.

---

## 6. Run All Test Parts

From repo root:

```bash
conda activate autograder

# Black-box (requires QuickCart server running)
QC_BASE_URL=http://localhost:8080 QC_ROLL_NUMBER=2024101103 pytest blackbox/tests/test_quickcart_api.py -q

# Integration
pytest integration/tests -q

# White-box
pytest whitebox/tests -q
```

---

## 7. Reports

- Black-box report: `blackbox/report.md`
- Integration report: `integration/report.md`
- White-box report: `whitebox/report.md`

---

## 8. Quick Command Reference

```bash
# Repo root
cd /home/arnav-agnihotri/Downloads/dass_testing/dass_testing

# Activate environment
conda activate autograder

# White-box tests
pytest whitebox/tests -q

# Integration tests
pytest integration/tests -q

# Black-box tests
QC_BASE_URL=http://localhost:8080 QC_ROLL_NUMBER=2024101103 pytest blackbox/tests/test_quickcart_api.py -q
```
GITHUB REPO LINK -https://github.com/cheetah671/dass_testing.git
ONE DRIVE LINK -https://drive.google.com/drive/folders/1jmtjgqPkAeC_kIF-b8k56B1ZqihPV2r0?usp=sharing
