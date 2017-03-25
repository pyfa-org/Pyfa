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
    assert StrongBluePillBooster.clear() == 'something?'




'''

class Booster(HandledItem, ItemAttrShortcut):

    @validates("ID", "itemID", "ammoID", "active")
    def validator(self, key, val):
        map = {"ID": lambda _val: isinstance(_val, int),
               "itemID": lambda _val: isinstance(_val, int),
               "ammoID": lambda _val: isinstance(_val, int),
               "active": lambda _val: isinstance(_val, bool),
               "slot": lambda _val: isinstance(_val, int) and 1 <= _val <= 3}

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val

    def __deepcopy__(self, memo):
        copy = Booster(self.item)
        copy.active = self.active

        return copy


'''