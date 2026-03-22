# MoneyPoly White-Box Testing Report

Date: 2026-03-22
Scope: `whitebox/moneypoly/moneypoly` (iterative file-by-file pylint fixes)

## Iteration 1 - `main.py`

- File: `whitebox/moneypoly/moneypoly/main.py`
- Pylint command: `PYTHONPATH=. pylint main.py`
- Initial findings:
	- `C0114`: missing module docstring
	- `C0116`: missing function docstring (`get_player_names`)
	- `C0116`: missing function docstring (`main`)
- Changes made:
	- Added module docstring at top of file.
	- Added docstring for `get_player_names()`.
	- Added docstring for `main()`.
- Score change: `8.24/10 -> 10.00/10`
- Commit message used:
	- `Iteration 1: Add module/function docstrings in main.py to resolve pylint missing-docstring warnings`

## Iteration 2 - `bank.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/bank.py`
- Pylint command: `PYTHONPATH=. pylint moneypoly/bank.py`
- Initial findings:
	- `C0114`: missing module docstring
	- `C0115`: missing class docstring (`Bank`)
	- `W0611`: unused import (`math`)
- Changes made:
	- Added module docstring.
	- Added class docstring for `Bank`.
	- Removed unused `math` import.
- Score change: `9.14/10 -> 10.00/10`
- Commit message used:
	- `Iteration 2: Add docstrings and remove unused import in bank.py`
