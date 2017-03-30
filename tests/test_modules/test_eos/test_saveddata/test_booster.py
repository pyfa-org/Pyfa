# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..', '..')))

# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
from _development.helpers_fits import RifterFit, KeepstarFit
from _development.helpers_items import StrongBluePillBooster


def test_itemModifiedAttributes(DB, StrongBluePillBooster):
    assert StrongBluePillBooster.itemModifiedAttributes is not None


def test_isInvalid(DB, StrongBluePillBooster):
    assert StrongBluePillBooster.isInvalid is False


def test_slot(DB, StrongBluePillBooster):
    assert StrongBluePillBooster.slot == 1


def test_item(DB, Gamedata, StrongBluePillBooster):
    assert isinstance(StrongBluePillBooster.item, Gamedata['Item'])


def test_clear(DB, StrongBluePillBooster):
    try:
        StrongBluePillBooster.clear()
        assert True
    except:
        assert False
