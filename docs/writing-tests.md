# Writing Tests for Pyfa

Writing tests for Pyfa is fairly simple. Follow these guidelines so tests stay maintainable and failures are easy to track.

Any rule can be broken, but there's a cost. If the cost is too high, the pull request may be rejected until the tests are rewritten.

## Write more tests

Nearly any code outside of the GUI can have tests. If you submit a PR, you are expected to add tests that cover the code in the PR. Sometimes this means writing broader tests, because your PR may only touch a small part of a method.

## One thing per test

Each test should target **one specific behavior**. Avoid lumping multiple behaviors into a single test. That increases run time but makes tests focused and makes it easier to find the root cause when they fail.

- **Good**: Many assert statements that all check one scenario (e.g. all attributes on a fit after adding a single module).
- **Bad**: Few assert statements spread across many steps (e.g. how a fit changes over time when adding multiple modules).

## Use helper fixtures

Use the existing helper fixtures instead of reimplementing setup. Request them as test parameters so pytest injects them.

To initialize the database and configure Eos:

```python
def test_example(DB):
    ...
```

This gives you a `DB` dictionary. Example: `DB['db'].getItem("Co-Processor II")`.

`Gamedata` and `Saveddata` work the same way. Example – get the "All 0" character:

```python
char0 = Saveddata['Character'].getAll0()
```

Available fixtures include: `DB`, `Gamedata`, `Saveddata`, `RifterFit`, `KeepstarFit`, `CurseFit`, `HeronFit`, `StrongBluePillBooster`. Define new ones in `_development/` when you need them.

## Name tests clearly

Test function names must start with `test_` or the test will not run.

Make the rest of the name descriptive. Recommended pattern:

**`test_<method or behavior under test>_<scenario>`**

- Bad: `test_newtest`
- Good: `test_getFitsWithShip_RifterFit` (we know the function and the scenario)

## Where tests go

Tests are split by purpose:

- **test_modules** – Mirrors the source layout. Low-level, method-specific tests.  
  If the code lives in `eos.saveddata.fit`, the test file is  
  `tests/test_modules/test_eos/test_saveddata/test_fit.py`.  
  Folder names under `test_modules` start with `test_` to avoid shadowing the real packages.

- **test_smoketests** – Higher-level tests that exercise a broad flow (e.g. a fit with a booster and a specific character) without targeting one method. Use this when you want to check that high-level actions work together.

## Clean up after yourself

Tests are not guaranteed to run in a fixed order. Any change to the environment (e.g. saving a fit to the DB) must be reverted before the test ends.

Example: save a fit, assert, then remove it.

```python
def test_getFitsWithShip_RifterFit(DB, RifterFit):
    DB['db'].save(RifterFit)
    assert Fit.getFitsWithShip(587)[0][1] == 'My Rifter Fit'
    DB['db'].remove(RifterFit)
```

If several tests need the same setup, use a class to group them and build the environment once.

## Running tests

1. Activate the project virtual environment:
   - **cmd.exe**: `PyfaEnv\scripts\activate.bat`
   - **PowerShell**: `PyfaEnv\Scripts\Activate.ps1`
   - **bash**: `source <venv>/Scripts/activate`

2. Install pytest (if needed):
   ```bash
   pip install pytest
   ```

3. From the project root (the directory containing `pyfa.py`), run:
   ```bash
   python -m pytest
   ```
   or
   ```bash
   py.test
   ```

To run only a subset of tests, pass a path or pattern, e.g. `python -m pytest tests/test_modules/test_service/`.
