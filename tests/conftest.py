import sys
import os
import pytest

# Ensure we modify sys environment for tests
sys._called_from_test = True

# Add root folder to python paths
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))

# Import fixtures from helpers
# DBInMemory is nicknamed DB in tests usually
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
from _development.helpers_fits import RifterFit, KeepstarFit, CurseFit, HeronFit
from _development.helpers_items import StrongBluePillBooster
