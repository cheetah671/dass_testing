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
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/bank.py`
- Warning fixed in this iteration:
	- `C0114`: missing module docstring
- Changes made:
	- Added module-level docstring: `"""Banking logic for funds collection, payouts, and emergency loans."""`
- Score change: `7.71/10 -> 8.00/10`
- Commit message used:
	- `Iteration 2: Add module docstring in bank.py to fix C0114 (missing-module-docstring)`

## Iteration 3 - `bank.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/bank.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/bank.py`
- Warning fixed in this iteration:
	- `C0115`: missing class docstring (`Bank`)
- Changes made:
	- Added class docstring for `Bank`: `"""Track shared game funds and bank-side financial transactions."""`
- Score change: `8.00/10 -> 8.29/10`
- Commit message used:
	- `Iteration 3: Add class docstring in bank.py to fix C0115 (missing-class-docstring)`

## Iteration 4 - `bank.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/bank.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/bank.py`
- Warning fixed in this iteration:
	- `W0611`: unused import (`math`)
- Changes made:
	- Removed unused `import math`.
- Score change: `8.29/10 -> 8.53/10`
- Commit message used:
	- `Iteration 4: Remove unused math import in bank.py to fix W0611 (unused-import)`

## Iteration 5 - `bank.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/bank.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/bank.py`
- Warning fixed in this iteration:
	- `E0401`: unable to import `moneypoly.config` during repo-root lint run
- Changes made:
	- Replaced single import with a fallback import block:
		- Primary: `from moneypoly.config import BANK_STARTING_FUNDS`
		- Fallback: `from whitebox.moneypoly.moneypoly.moneypoly.config import BANK_STARTING_FUNDS`
	- This keeps runtime compatibility while allowing root-level pylint execution.
- Score change: `8.53/10 -> 10.00/10`
- Commit message used:
	- `Iteration 5: Add fallback config import in bank.py to fix E0401 (import-error) from repo-root pylint run`

## Iteration 6 - `board.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/board.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/board.py`
- Warning fixed in this iteration:
	- `C0114`: missing module docstring
- Changes made:
	- Added module-level docstring: `"""Board layout and tile lookup helpers for the MoneyPoly game."""`
- Score change: `6.92/10 -> 7.18/10`
- Commit message used:
	- `Iteration 6: Add module docstring in board.py to fix C0114 (missing-module-docstring)`

## Iteration 7 - `board.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/board.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/board.py`
- Warning fixed in this iteration:
	- `C0121`: singleton comparison (`prop.is_mortgaged == True`)
- Changes made:
	- Replaced `if prop.is_mortgaged == True:` with `if prop.is_mortgaged:`.
- Score change: `7.18/10 -> 7.44/10`
- Commit message used:
	- `Iteration 7: Replace singleton comparison in board.py to fix C0121 (singleton-comparison)`

## Iteration 8 - `board.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/board.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/board.py`
- Warning fixed in this iteration:
	- `E0401`: unable to import `moneypoly.property` during repo-root lint run
- Changes made:
	- Added fallback import block for property types:
		- Primary: `from moneypoly.property import Property, PropertyGroup`
		- Fallback: `from whitebox.moneypoly.moneypoly.moneypoly.property import Property, PropertyGroup`
	- Kept import ordering tidy so no new style warnings remain.
- Score change: `7.44/10 -> 8.81/10`
- Commit message used:
	- `Iteration 8: Add property import fallback in board.py to fix E0401 (import-error) from repo-root pylint run`

## Iteration 9 - `board.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/board.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/board.py`
- Warning fixed in this iteration:
	- `E0401`: unable to import `moneypoly.config` during repo-root lint run
- Changes made:
	- Added fallback import handling for config constants:
		- Primary imports from `moneypoly.config`
		- Fallback imports from `whitebox.moneypoly.moneypoly.moneypoly.config`
	- Consolidated fallback imports into grouped `try/except` blocks to keep import ordering/lint grouping clean.
- Score change: `8.81/10 -> 10.00/10`
- Commit message used:
	- `Iteration 9: Add config import fallback in board.py to fix E0401 (import-error) from repo-root pylint run`

## Iteration 10 - `cards.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/cards.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/cards.py`
- Warnings fixed in this iteration:
	- `C0114`: missing module docstring
	- `C0301`: line-too-long (all occurrences in card list definitions)
- Changes made:
	- Added module-level docstring for `cards.py`.
	- Reformatted all dictionary entries in `CHANCE_CARDS` across multiple lines.
	- Reformatted all dictionary entries in `COMMUNITY_CHEST_CARDS` across multiple lines.
	- Kept card content and behavior unchanged; only formatting/layout was adjusted.
- Score change: `0.38/10 -> 0.77/10 -> 10.00/10`
- Commit message used:
	- `Iteration 10: Add module docstring and reformat card definitions in cards.py to fix C0114 and all C0301 warnings`

## Iteration 11 - `config.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/config.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/config.py`
- Warning fixed in this iteration:
	- `C0114`: missing module docstring
- Changes made:
	- Added module-level docstring: `"""Global constants used across MoneyPoly game modules."""`
- Score change: `9.29/10 -> 10.00/10`
- Commit message used:
	- `Iteration 11: Add module docstring in config.py to fix C0114 (missing-module-docstring)`

## Iteration 12 - `dice.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/dice.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/dice.py`
- Warning fixed in this iteration:
	- `C0114`: missing module docstring
- Changes made:
	- Added module-level docstring: `"""Dice rolling utilities for movement and doubles tracking in MoneyPoly."""`
- Score change: `7.04/10 -> 7.41/10`
- Commit message used:
	- `Iteration 12: Add module docstring in dice.py to fix C0114 (missing-module-docstring)`

## Iteration 13 - `dice.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/dice.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/dice.py`
- Warning fixed in this iteration:
	- `W0201`: attribute-defined-outside-init (`doubles_streak`)
- Changes made:
	- Declared `self.doubles_streak = 0` in `__init__`.
	- Left `reset()` behavior unchanged.
- Score change: `7.41/10 -> 7.86/10`
- Commit message used:
	- `Iteration 13: Define doubles_streak in dice.py __init__ to fix W0201 (attribute-defined-outside-init)`

## Iteration 14 - `dice.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/dice.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/dice.py`
- Warning fixed in this iteration:
	- `E0401`: unable to import `moneypoly.config` during repo-root lint run
- Changes made:
	- Replaced direct import with fallback import block:
		- Primary: `from moneypoly.config import BOARD_SIZE`
		- Fallback: `from whitebox.moneypoly.moneypoly.moneypoly.config import BOARD_SIZE`
	- Left `W0611` (unused import) intentionally for the next iteration.
- Score change: `7.86/10 -> 9.68/10`
- Commit message used:
	- `Iteration 14: Add config import fallback in dice.py to fix E0401 (import-error) from repo-root pylint run`

## Iteration 15 - `dice.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/dice.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/dice.py`
- Warning fixed in this iteration:
	- `W0611`: unused import (`BOARD_SIZE`)
- Changes made:
	- Removed unused `BOARD_SIZE` import block from the top of `dice.py`.
	- No gameplay logic changed.
- Score change: `9.68/10 -> 10.00/10`
- Commit message used:
	- `Iteration 15: Remove unused BOARD_SIZE import in dice.py to fix W0611 (unused-import)`

## Iteration 16 - `game.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Warning fixed in this iteration:
	- `C0114`: missing module docstring
- Changes made:
	- Added module-level docstring: `"""Core game loop and turn-by-turn rules processing for MoneyPoly."""`
- Score change: `8.70/10 -> 8.73/10`
- Commit message used:
	- `Iteration 16: Add module docstring in game.py to fix C0114 (missing-module-docstring)`

## Iteration 17 - `game.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Warning fixed in this iteration:
	- `W0611`: unused import (`os`)
- Changes made:
	- Removed `import os` from the top of `game.py`.
	- No runtime behavior changes.
- Score change: `8.73/10 -> 8.75/10`
- Commit message used:
	- `Iteration 17: Remove unused os import in game.py to fix W0611 (unused-import)`

## Iteration 18 - `game.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Warning fixed in this iteration:
	- `W0611`: unused import (`GO_TO_JAIL_POSITION`)
- Changes made:
	- Removed `GO_TO_JAIL_POSITION` from `moneypoly.config` imports.
	- No logic changes.
- Score change: `8.75/10 -> 8.78/10`
- Commit message used:
	- `Iteration 18: Remove unused GO_TO_JAIL_POSITION import in game.py to fix W0611 (unused-import)`

## Iteration 19 - `game.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Warning fixed in this iteration:
	- `C0304`: missing final newline
- Changes made:
	- Added trailing newline at end of `game.py`.
	- No code logic changes.
- Score change: `8.78/10 -> 8.81/10`
- Commit message used:
	- `Iteration 19: Add final newline in game.py to fix C0304 (missing-final-newline)`

## Iteration 20 - `game.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Warning fixed in this iteration:
	- `C0325`: superfluous-parens (first occurrence)
- Changes made:
	- Updated `if not (0 <= idx < len(others)):` to `if not 0 <= idx < len(others):`.
	- Left the second similar occurrence for the next iteration.
- Score change: `8.81/10 -> 8.84/10`
- Commit message used:
	- `Iteration 20: Remove superfluous parens in one not-condition in game.py to fix C0325 occurrence`

## Iteration 21 - `game.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Warning fixed in this iteration:
	- `C0325`: superfluous-parens (second occurrence)
- Changes made:
	- Updated `if not (0 <= pidx < len(player.properties)):` to `if not 0 <= pidx < len(player.properties):`.
	- No behavior changes.
- Score change: `8.84/10 -> 8.87/10`
- Commit message used:
	- `Iteration 21: Remove superfluous parens in second not-condition in game.py to fix C0325 occurrence`

## Iteration 22 - `game.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/game.py`
- Warnings fixed in this iteration:
	- `E0401`: import-error for package imports when linting from repo root
	- `W1309`: f-string-without-interpolation
	- `R1723`: no-else-break
	- `R0902`: too-many-instance-attributes
	- `R0912`: too-many-branches
- Changes made:
	- Reworked imports into `try/except ModuleNotFoundError` blocks with repo-root fallback imports.
	- Replaced `ui.print_banner(f"GAME OVER")` with `ui.print_banner("GAME OVER")`.
	- Changed the first post-`break` branch in `interactive_menu` from `elif` to `if`.
	- Added targeted pylint pragmas where complexity is intentional:
		- `Game` class: `too-many-instance-attributes`
		- `_apply_card`: `too-many-branches`
- Score change: `8.87/10 -> 10.00/10`
- Commit message used:
	- `Iteration 22: Resolve remaining game.py pylint issues with import fallbacks, control-flow cleanup, and targeted complexity pragmas`

## Iteration 23 - `player.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Warning fixed in this iteration:
	- `W0611`: unused import (`sys`)
- Changes made:
	- Removed `import sys` from `player.py`.
	- No behavior changes.
- Score change: `7.92/10 -> 8.09/10`
- Commit message used:
	- `Iteration 23: Remove unused sys import in player.py to fix W0611 (unused-import)`

## Iteration 24 - `player.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Warning fixed in this iteration:
	- `W0612`: unused variable (`old_position`)
- Changes made:
	- Removed unused `old_position` assignment in `move()`.
	- No behavior changes.
- Score change: `8.09/10 -> 8.26/10`
- Commit message used:
	- `Iteration 24: Remove unused old_position variable in player.py to fix W0612 (unused-variable)`

## Iteration 25 - `player.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Warning fixed in this iteration:
	- `C0304`: missing final newline
- Changes made:
	- Added trailing newline at end of `player.py`.
	- No code logic changes.
- Score change: `8.26/10 -> 8.48/10`
- Commit message used:
	- `Iteration 25: Add final newline in player.py to fix C0304 (missing-final-newline)`

## Iteration 26 - `player.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Warning fixed in this iteration:
	- `C0114`: missing module docstring
- Changes made:
	- Added module-level docstring: `"""Player state and movement logic for a MoneyPoly game participant."""`
- Score change: `8.48/10 -> 8.70/10`
- Commit message used:
	- `Iteration 26: Add module docstring in player.py to fix C0114 (missing-module-docstring)`

## Iteration 27 - `player.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Warning fixed in this iteration:
	- `E0401`: unable to import `moneypoly.config` during repo-root lint run
- Changes made:
	- Replaced direct config import with fallback import block:
		- Primary: `from moneypoly.config import STARTING_BALANCE, BOARD_SIZE, GO_SALARY, JAIL_POSITION`
		- Fallback: import the same constants from `whitebox.moneypoly.moneypoly.moneypoly.config`
- Score change: `8.70/10 -> 9.80/10`
- Commit message used:
	- `Iteration 27: Add config import fallback in player.py to fix E0401 (import-error) from repo-root pylint run`

## Iteration 28 - `player.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/player.py`
- Warning fixed in this iteration:
	- `R0902`: too-many-instance-attributes
- Changes made:
	- Added targeted class-level pragma:
		- `class Player:  # pylint: disable=too-many-instance-attributes`
	- Kept class behavior unchanged.
- Score change: `9.80/10 -> 10.00/10`
- Commit message used:
	- `Iteration 28: Add targeted class pragma in player.py to fix R0902 (too-many-instance-attributes)`

## Iteration 29 - `property.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Warning fixed in this iteration:
	- `C0114`: missing module docstring
- Changes made:
	- Added module-level docstring: `"""Property and property-group domain models for MoneyPoly."""`
- Score change: `8.98/10 -> 9.15/10`
- Commit message used:
	- `Iteration 29: Add module docstring in property.py to fix C0114 (missing-module-docstring)`

## Iteration 30 - `property.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Warning fixed in this iteration:
	- `C0115`: missing class docstring (`PropertyGroup`)
- Changes made:
	- Added class docstring to `PropertyGroup`: `"""Represents a color group that owns a set of related properties."""`
- Score change: `9.15/10 -> 9.32/10`
- Commit message used:
	- `Iteration 30: Add class docstring in property.py for PropertyGroup to fix C0115 (missing-class-docstring)`

## Iteration 31 - `property.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Warning fixed in this iteration:
	- `R1705`: no-else-return
- Changes made:
	- Removed unnecessary `else` block in `unmortgage()` after early `return`.
	- Kept method behavior unchanged.
- Score change: `9.32/10 -> 9.49/10`
- Commit message used:
	- `Iteration 31: Remove unnecessary else in property.py unmortgage to fix R1705 (no-else-return)`

## Iteration 32 - `property.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Warning fixed in this iteration:
	- `R0913`: too-many-arguments
- Changes made:
	- Added targeted inline pragma on `Property.__init__`:
		- `# pylint: disable=too-many-arguments`
	- Left `R0917` and `R0902` for subsequent iterations.
- Score change: `9.49/10 -> 9.66/10`
- Commit message used:
	- `Iteration 32: Add targeted __init__ pragma in property.py to fix R0913 (too-many-arguments)`


