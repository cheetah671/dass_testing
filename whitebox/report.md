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

## Iteration 33 - `property.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Warning fixed in this iteration:
	- `R0917`: too-many-positional-arguments
- Changes made:
	- Extended `Property.__init__` inline pragma to include `too-many-positional-arguments`.
	- Updated pragma:
		- `# pylint: disable=too-many-arguments,too-many-positional-arguments`
- Score change: `9.66/10 -> 9.83/10`
- Commit message used:
	- `Iteration 33: Extend __init__ pragma in property.py to fix R0917 (too-many-positional-arguments)`

## Iteration 34 - `property.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/property.py`
- Warning fixed in this iteration:
	- `R0902`: too-many-instance-attributes
- Changes made:
	- Added targeted class-level pragma on `Property`:
		- `class Property:  # pylint: disable=too-many-instance-attributes`
	- No logic changes.
- Score change: `9.83/10 -> 10.00/10`
- Commit message used:
	- `Iteration 34: Add targeted class pragma in property.py to fix R0902 (too-many-instance-attributes)`

## Iteration 35 - `ui.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/ui.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/ui.py`
- Warning fixed in this iteration:
	- `C0114`: missing module docstring
- Changes made:
	- Added module-level docstring: `"""Console UI helpers for displaying MoneyPoly game state and prompts."""`
- Score change: `9.55/10 -> 9.77/10`
- Commit message used:
	- `Iteration 35: Add module docstring in ui.py to fix C0114 (missing-module-docstring)`

## Iteration 36 - `ui.py`

- File: `whitebox/moneypoly/moneypoly/moneypoly/ui.py`
- Pylint command: `pylint whitebox/moneypoly/moneypoly/moneypoly/ui.py`
- Warning fixed in this iteration:
	- `W0702`: bare-except
- Changes made:
	- Replaced bare `except:` with `except ValueError:` in `safe_int_input()`.
	- Preserved existing fallback behavior (`return default`) for invalid integer input.
- Score change: `9.77/10 -> 10.00/10`
- Commit message used:
	- `Iteration 36: Replace bare except in ui.py safe_int_input to fix W0702 (bare-except)`

## Final Validation

- Command run:
	- `pylint whitebox/moneypoly/moneypoly/main.py whitebox/moneypoly/moneypoly/moneypoly/*.py`
- Final result:
	- `10.00/10`
- Note:
	- This confirms all iterative fixes (Iterations 1 through 36) produce a clean lint result across the MoneyPoly entrypoint and all package modules.

## 1.3 White-Box Test Design (Updated After Suite Refactor)

- Goal:
	- Keep 1.3 focused on branch/decision-path testing before bug fixes.
	- Document the full current failure state after test-suite restructuring and import normalization.

- Test suite changes in this update:
	- Imports in tests were normalized from `moneypoly.moneypoly.moneypoly...` to `moneypoly...`.
	- `whitebox/tests/conftest.py` now bootstraps `sys.path` to load package modules consistently across terminal contexts.
	- Additional decision-path and integration files are now part of active 1.3 coverage:
		- `whitebox/tests/test_game.py`
		- `whitebox/tests/test_game_decision_path.py`
		- `whitebox/tests/test_integration.py`
		- `whitebox/tests/test_integration_decision_path.py`
		- `whitebox/tests/test_integration_extra.py`
		- `whitebox/tests/test_remaining_decision_path.py`

- Command run:
	- `pytest whitebox/tests -q`

- Latest baseline result:
	- `288` tests executed
	- `251` passed, `37` failed

### Updated Error Inventory (37/37)

1. Error 1 - `whitebox/tests/test_bank.py::test_collect_negative_amounts_are_ignored[-1]`
	- Why this test is needed (simple): negative collection should never reduce bank money.
	- Observed failure: bank balance decreases after `collect(-1)`.
	- Logical issue found: `Bank.collect()` accepts negative values without validation.

2. Error 2 - `whitebox/tests/test_bank.py::test_collect_negative_amounts_are_ignored[-5]`
	- Why this test is needed (simple): invalid medium negative amounts must also be blocked.
	- Observed failure: bank balance decreases after `collect(-5)`.
	- Logical issue found: same missing negative-value guard in `collect`.

3. Error 3 - `whitebox/tests/test_bank.py::test_collect_negative_amounts_are_ignored[-200]`
	- Why this test is needed (simple): large invalid negative values must not corrupt funds.
	- Observed failure: bank balance decreases after `collect(-200)`.
	- Logical issue found: invalid signed input path still mutates `_funds`.

4. Error 4 - `whitebox/tests/test_cards.py::test_empty_deck_cards_remaining_is_zero`
	- Why this test is needed (simple): empty decks should be safe and report zero remaining cards.
	- Observed failure: `ZeroDivisionError` in `cards_remaining()`.
	- Logical issue found: modulo/division performed with `len(self.cards)` when deck is empty.

5. Error 5 - `whitebox/tests/test_game.py::test_move_and_resolve_dispatches_tile_handlers[go_to_jail-jail]`
	- Why this test is needed (simple): tile dispatch should call a dedicated jail handler path.
	- Observed failure: `Game` has no attribute `_handle_go_to_jail_tile`.
	- Logical issue found: tests expect decomposed tile handlers, but implementation is inlined in `_move_and_resolve`.

6. Error 6 - `whitebox/tests/test_game.py::test_move_and_resolve_dispatches_tile_handlers[income_tax-income]`
	- Why this test is needed (simple): income tax branch should be independently dispatchable.
	- Observed failure: missing `_handle_income_tax_tile`-style handler attribute.
	- Logical issue found: no dedicated handler method exists for monkeypatchable dispatch path.

7. Error 7 - `whitebox/tests/test_game.py::test_move_and_resolve_dispatches_tile_handlers[luxury_tax-luxury]`
	- Why this test is needed (simple): luxury tax flow should be independently testable.
	- Observed failure: missing dedicated luxury-tax tile handler attribute.
	- Logical issue found: same handler decomposition gap as above.

8. Error 8 - `whitebox/tests/test_game.py::test_move_and_resolve_dispatches_tile_handlers[free_parking-parking]`
	- Why this test is needed (simple): free parking branch should be explicitly dispatch-tested.
	- Observed failure: expected handler attribute not found.
	- Logical issue found: inlined branching prevents expected handler-level instrumentation.

9. Error 9 - `whitebox/tests/test_game.py::test_move_and_resolve_dispatches_tile_handlers[chance-chance]`
	- Why this test is needed (simple): chance tile should call clear card-draw/handler path.
	- Observed failure: handler monkeypatch target missing.
	- Logical issue found: interface mismatch between refactored tests and current game internals.

10. Error 10 - `whitebox/tests/test_game.py::test_move_and_resolve_dispatches_tile_handlers[community_chest-chest]`
	- Why this test is needed (simple): chest tile should follow explicit dispatch contract.
	- Observed failure: missing expected handler attribute.
	- Logical issue found: same dispatch API mismatch as other tile-handler tests.

11. Error 11 - `whitebox/tests/test_game.py::test_buy_property_succeeds_when_balance_equals_price`
	- Why this test is needed (simple): exact-balance players should be able to buy a property.
	- Observed failure: buy returns false when `balance == price`.
	- Logical issue found: affordability condition is too strict (`<=` instead of `<`).

12. Error 12 - `whitebox/tests/test_game.py::test_find_winner_returns_highest_net_worth_player`
	- Why this test is needed (simple): winner must be richest player.
	- Observed failure: lower net-worth player returned.
	- Logical issue found: winner calculation uses `min` net worth.

13. Error 13 - `whitebox/tests/test_game_decision_path.py::test_draw_and_apply_uses_selected_deck`
	- Why this test is needed (simple): game should expose/select decks consistently for draw/apply logic.
	- Observed failure: `Game` has no `decks` attribute.
	- Logical issue found: expected deck abstraction in tests is absent in implementation.

14. Error 14 - `whitebox/tests/test_game_decision_path.py::test_apply_card_birthday_alias_calls_collect_from_others`
	- Why this test is needed (simple): birthday behavior should map to shared collect-from-others logic.
	- Observed failure: missing expected card helper method/attribute path.
	- Logical issue found: helper-level card API expected by tests is not implemented.

15. Error 15 - `whitebox/tests/test_integration.py::test_integration_bank_loan_updates_player_and_bank_balance`
	- Why this test is needed (simple): loan should transfer money from bank to player.
	- Observed failure: bank balance unchanged after loan issue.
	- Logical issue found: `Bank.give_loan()` does not debit bank funds.

16. Error 16 - `whitebox/tests/test_integration.py::test_integration_purchase_then_rent_transfers_to_owner`
	- Why this test is needed (simple): rent should increase owner balance.
	- Observed failure: owner not credited after tenant pays rent.
	- Logical issue found: `Game.pay_rent()` deducts tenant balance but omits owner credit.

17. Error 17 - `whitebox/tests/test_integration.py::test_integration_trade_transfers_cash_and_property`
	- Why this test is needed (simple): successful trade must move both cash and property.
	- Observed failure: seller cash does not increase as expected.
	- Logical issue found: `trade()` deducts buyer but does not credit seller.

18. Error 18 - `whitebox/tests/test_integration.py::test_integration_collect_from_all_transfers_from_each_eligible_player`
	- Why this test is needed (simple): collect-from-all card logic should be reusable and correct.
	- Observed failure: missing `_card_collect_from_others` helper.
	- Logical issue found: helper API assumed by tests is missing in implementation.

19. Error 19 - `whitebox/tests/test_integration.py::test_integration_card_move_to_property_and_buy`
	- Why this test is needed (simple): move-to card should route property landing behavior correctly.
	- Observed failure: missing `_card_move_to` helper.
	- Logical issue found: card movement is embedded in `_apply_card`; helper interface absent.

20. Error 20 - `whitebox/tests/test_integration.py::test_integration_card_collect_uses_bank_payout_path`
	- Why this test is needed (simple): collect card should use bank payout path consistently.
	- Observed failure: missing `_card_collect` helper.
	- Logical issue found: card sub-action helper expected by tests is absent.

21. Error 21 - `whitebox/tests/test_integration_decision_path.py::test_integration_card_collect_from_all_skips_collector_and_low_balance_players`
	- Why this test is needed (simple): low-balance players should be skipped safely in collect-from-all.
	- Observed failure: missing `_card_collect_from_others` helper.
	- Logical issue found: same helper-interface gap as Errors 18 and 20.

22. Error 22 - `whitebox/tests/test_integration_decision_path.py::test_integration_card_move_to_property_skip_branch`
	- Why this test is needed (simple): move-to property skip choice should be directly testable.
	- Observed failure: missing `_card_move_to` helper.
	- Logical issue found: no dedicated card-move helper exposed for branch-level testing.

23. Error 23 - `whitebox/tests/test_integration_decision_path.py::test_integration_card_move_to_go_tile_collects_salary_without_prompt`
	- Why this test is needed (simple): GO wrap salary from card-move should work without UI blocking.
	- Observed failure: missing `_card_move_to` helper.
	- Logical issue found: helper-level API absent; card logic tightly coupled inside `_apply_card`.

24. Error 24 - `whitebox/tests/test_integration_extra.py::test_integration_move_and_resolve_income_tax_reduces_player_and_increases_bank`
	- Why this test is needed (simple): income tax tile should be unit-isolated and deterministic.
	- Observed failure: missing `_handle_income_tax_tile` helper.
	- Logical issue found: handler decomposition expected in tests does not exist.

25. Error 25 - `whitebox/tests/test_integration_extra.py::test_integration_move_and_resolve_luxury_tax_reduces_player_and_increases_bank`
	- Why this test is needed (simple): luxury tax tile should be independently validated.
	- Observed failure: missing `_handle_luxury_tax_tile` helper.
	- Logical issue found: same tile-handler API mismatch as above.

26. Error 26 - `whitebox/tests/test_integration_extra.py::test_integration_card_move_to_same_or_forward_does_not_collect_go_salary`
	- Why this test is needed (simple): no salary should be awarded if GO is not crossed.
	- Observed failure: missing `_card_move_to` helper.
	- Logical issue found: absence of dedicated helper blocks direct verification.

27. Error 27 - `whitebox/tests/test_integration_extra.py::test_integration_card_move_to_wrap_collects_go_salary`
	- Why this test is needed (simple): crossing GO via card should award salary.
	- Observed failure: missing `_card_move_to` helper.
	- Logical issue found: card move logic is not exposed through expected helper API.

28. Error 28 - `whitebox/tests/test_integration_extra.py::test_integration_draw_and_apply_none_card_is_noop`
	- Why this test is needed (simple): draw/apply should safely no-op on empty card draw.
	- Observed failure: `Game` has no `decks` attribute.
	- Logical issue found: test expects dictionary-based deck access; implementation uses separate deck fields.

29. Error 29 - `whitebox/tests/test_player.py::test_move_wraps_board_and_passes_go_collects_salary`
	- Why this test is needed (simple): passing GO during wrap must pay salary.
	- Observed failure: balance unchanged after move from 39 to 1.
	- Logical issue found: `Player.move()` only pays salary when landing exactly on 0.

30. Error 30 - `whitebox/tests/test_property.py::test_group_all_owned_by_requires_every_property_owned_by_player`
	- Why this test is needed (simple): full-group ownership must require every property.
	- Observed failure: method returns true on mixed ownership.
	- Logical issue found: `all_owned_by()` uses `any(...)` instead of all-members check.

31. Error 31 - `whitebox/tests/test_property.py::test_get_rent_doubles_only_on_full_group_ownership`
	- Why this test is needed (simple): rent should double only for true monopoly ownership.
	- Observed failure: doubled rent returned despite partial ownership.
	- Logical issue found: rent calculation depends on flawed `all_owned_by()` behavior.

32. Error 32 - `whitebox/tests/test_remaining_decision_path.py::test_tile_handlers_direct_paths_cover_jail_income_luxury_and_free_parking`
	- Why this test is needed (simple): direct tile handler calls improve branch-level reliability.
	- Observed failure: missing `_handle_go_to_jail_tile` helper.
	- Logical issue found: expected helper API is not present in current Game design.

33. Error 33 - `whitebox/tests/test_remaining_decision_path.py::test_mortgage_property_rejects_when_bank_cannot_pay`
	- Why this test is needed (simple): mortgage payout should fail if bank has no funds.
	- Observed failure: mortgage succeeds even when bank reserves are zero.
	- Logical issue found: mortgage flow credits player without checking bank payout capability.

34. Error 34 - `whitebox/tests/test_remaining_decision_path.py::test_card_move_to_property_tile_with_missing_property_no_handler_call`
	- Why this test is needed (simple): move-to should handle missing property lookup safely.
	- Observed failure: missing `_card_move_to` helper.
	- Logical issue found: no dedicated helper for guarded card movement branch.

35. Error 35 - `whitebox/tests/test_remaining_decision_path.py::test_card_collect_from_others_ignores_underfunded_players`
	- Why this test is needed (simple): underfunded players should be skipped in mass-collect operations.
	- Observed failure: missing `_card_collect_from_others` helper.
	- Logical issue found: helper-level card collection API absent.

36. Error 36 - `whitebox/tests/test_remaining_decision_path.py::test_unmortgage_fails_when_insufficient_balance_keeps_mortgaged`
	- Why this test is needed (simple): failed unmortgage must keep property mortgaged.
	- Observed failure: unmortgage failure path leaves property as not mortgaged.
	- Logical issue found: `unmortgage_property()` calls `prop.unmortgage()` before checking player affordability, causing incorrect state mutation on failure.

37. Error 37 - `whitebox/tests/test_remaining_decision_path.py::test_card_move_to_non_property_tile_does_not_call_property_handler`
	- Why this test is needed (simple): non-property card destinations must not invoke property flow.
	- Observed failure: missing `_card_move_to` helper.
	- Logical issue found: card routing helper expected by tests is not implemented.

### Summary Of Current 1.3 Findings

- Confirmed gameplay logic defects:
	- Negative `Bank.collect` handling.
	- Loan does not debit bank reserves.
	- Trade does not credit seller cash.
	- Rent does not credit owner.
	- GO salary miss when passing GO (non-zero wrap).
	- Winner selection uses minimum net worth.
	- Group ownership uses partial (`any`) instead of full ownership.
	- Empty deck `cards_remaining()` divides by zero.
	- Unmortgage failure mutates mortgage state incorrectly.
	- Mortgage payout does not enforce bank affordability.

- Architecture/test-contract mismatches introduced by expanded suite:
	- Missing helper methods expected by new tests: `_card_move_to`, `_card_collect`, `_card_collect_from_others`, `_handle_go_to_jail_tile`, `_handle_income_tax_tile`, `_handle_luxury_tax_tile`, and `decks` mapping abstraction.
	- These are currently recorded as 1.3 failures and must be resolved either by:
		- implementing the helper API in code, or
		- adapting tests to current inlined architecture (if helper API is intentionally out-of-scope).

## 1.3 Fix Execution Log (13 Batches)

- Fix strategy note:
	- Errors were fixed in 13 incremental batches and validated after each batch.
	- Numbering below follows the final fix-order used during implementation (`Error 1` to `Error 13`).

1. Error 1: Ignore negative bank collection inputs.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/bank.py`
	- Change: `Bank.collect()` now returns early for negative amounts.
	- Effect: prevents invalid negative collect values from reducing bank funds.

2. Error 2: Handle empty deck safely in `cards_remaining`.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/cards.py`
	- Change: `CardDeck.cards_remaining()` returns `0` when deck is empty.
	- Effect: removes `ZeroDivisionError` for empty-deck paths.

3. Error 3: Debit bank funds when issuing emergency loans.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/bank.py`
	- Change: `Bank.give_loan()` now reduces bank reserves by the loan amount.
	- Effect: loan flow is now a real transfer (bank -> player), not money creation.

4. Error 4: Add tile-handler and deck-dispatch APIs expected by suite.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
	- Changes:
		- Added `self.decks` mapping.
		- Added `_draw_and_apply(...)`.
		- Added `_handle_go_to_jail_tile`, `_handle_income_tax_tile`, `_handle_luxury_tax_tile`, `_handle_free_parking_tile`.
		- Routed `_move_and_resolve(...)` through these handlers.
	- Effect: resolved missing-attribute branch-dispatch failures and aligned code with test contract.

5. Error 5: Allow exact-balance property purchase.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
	- Change: `buy_property()` affordability check updated from `<=` to `<`.
	- Effect: player can buy when `balance == price`.

6. Error 6: Add card helper APIs and route `_apply_card` through them.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
	- Changes:
		- Added `_card_collect`, `_card_collect_from_others`, `_card_move_to`.
		- Updated `_apply_card(...)` to call these helpers.
	- Effect: fixed missing card-helper attributes and stabilized card action paths.

7. Error 7: Correct winner selection logic.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
	- Change: `find_winner()` now uses `max(..., key=net_worth)`.
	- Effect: highest net-worth player is selected as winner.

8. Error 8: Credit owner during rent payment.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
	- Change: `pay_rent()` now adds rent to `prop.owner` after tenant deduction.
	- Effect: rent is transferred correctly instead of disappearing.

9. Error 9: Credit seller during successful trade.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
	- Change: `trade()` now calls `seller.add_money(cash_amount)`.
	- Effect: trade cash flow is now complete (buyer -> seller).

10. Error 10: Award GO salary on wraparound movement.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/player.py`
	- Change: `move()` now awards salary when crossing GO (`new_pos < old_pos`) or landing on GO.
	- Effect: correct salary behavior for wraparound movement.

11. Error 11: Require full group ownership.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/property.py`
	- Change: `PropertyGroup.all_owned_by()` now uses `all(...)` with non-empty guard.
	- Effect: rent multiplier now triggers only on true full-group ownership.

12. Error 12: Enforce bank liquidity for mortgage payout.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
	- Changes:
		- `mortgage_property()` now uses `bank.pay_out(payout)`.
		- Rolls back mortgage flag if bank cannot pay.
	- Effect: mortgage fails safely when bank reserves are insufficient.

13. Error 13: Preserve mortgage state on failed unmortgage.
	- File: `whitebox/moneypoly/moneypoly/moneypoly/game.py`
	- Changes:
		- `unmortgage_property()` now checks affordability before clearing mortgage status.
		- Sets `prop.is_mortgaged = False` only after successful payment.
	- Effect: failed unmortgage no longer mutates property state incorrectly.

### Final Verification After 13 Batches

- Command:
	- `pytest whitebox/tests -q`
- Result:
	- `288 passed`
	- `0 failed`


