"""
Pytest configuration for Pyfa tests.
Ensures project root and _development are on sys.path and exposes shared fixtures.
Tests can request DB, Gamedata, Saveddata, RifterFit, KeepstarFit, etc. by name.
"""
import os
import sys

# Project root = parent of tests/ (so _development can be imported)
_root = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if _root not in sys.path:
    sys.path.insert(0, _root)

# Register fixtures from _development (DBInMemory, Gamedata, Saveddata, fit and item fixtures)
pytest_plugins = [
    '_development.helpers',
    '_development.helpers_fits',
    '_development.helpers_items',
]

import pytest


@pytest.fixture
def DB(DBInMemory):
    """Alias for DBInMemory so tests can request 'DB' by name."""
    return DBInMemory
