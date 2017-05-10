# TODO: Drop the `_2` from the file name once one of our fit files are renamed

# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys
from copy import deepcopy

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..', '..')))

# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
from _development.helpers_fits import RifterFit, KeepstarFit, HeronFit


def test_calculateModifiedAttributes(DB, RifterFit, KeepstarFit):
    rifter_modifier_dicts = {
        '_ModifiedAttributeDict__affectedBy'          : 26,
        '_ModifiedAttributeDict__forced'              : 0,
        '_ModifiedAttributeDict__intermediary'        : 0,
        '_ModifiedAttributeDict__modified'            : 26,
        '_ModifiedAttributeDict__multipliers'         : 22,
        '_ModifiedAttributeDict__overrides'           : 0,
        '_ModifiedAttributeDict__penalizedMultipliers': 0,
        '_ModifiedAttributeDict__postIncreases'       : 0,
        '_ModifiedAttributeDict__preAssigns'          : 0,
        '_ModifiedAttributeDict__preIncreases'        : 4,
    }

    # Test before calculating attributes
    for test_dict in rifter_modifier_dicts:
        assert len(getattr(RifterFit.ship.itemModifiedAttributes, test_dict)) == 0

    RifterFit.calculateModifiedAttributes()

    for test_dict in rifter_modifier_dicts:
        assert len(getattr(RifterFit.ship.itemModifiedAttributes, test_dict)) == rifter_modifier_dicts[test_dict]

    # Keepstars don't have any basic skills that would change their attributes
    keepstar_modifier_dicts = {
        '_ModifiedAttributeDict__affectedBy'          : 0,
        '_ModifiedAttributeDict__forced'              : 0,
        '_ModifiedAttributeDict__intermediary'        : 0,
        '_ModifiedAttributeDict__modified'            : 0,
        '_ModifiedAttributeDict__multipliers'         : 0,
        '_ModifiedAttributeDict__overrides'           : 0,
        '_ModifiedAttributeDict__penalizedMultipliers': 0,
        '_ModifiedAttributeDict__postIncreases'       : 0,
        '_ModifiedAttributeDict__preAssigns'          : 0,
        '_ModifiedAttributeDict__preIncreases'        : 0,
    }

    # Test before calculating attributes
    for test_dict in keepstar_modifier_dicts:
        assert len(getattr(KeepstarFit.ship.itemModifiedAttributes, test_dict)) == 0

    KeepstarFit.calculateModifiedAttributes()

    for test_dict in keepstar_modifier_dicts:
        assert len(getattr(KeepstarFit.ship.itemModifiedAttributes, test_dict)) == keepstar_modifier_dicts[test_dict]

def test_calculateModifiedAttributes_withProjected(DB, RifterFit, HeronFit):
    # TODO: This test is not currently functional or meaningful as projections are not happening correctly.
    # This is true for all tested branches (master, dev, etc)
    rifter_modifier_dicts = {
        '_ModifiedAttributeDict__affectedBy'          : 26,
        '_ModifiedAttributeDict__forced'              : 0,
        '_ModifiedAttributeDict__intermediary'        : 0,
        '_ModifiedAttributeDict__modified'            : 26,
        '_ModifiedAttributeDict__multipliers'         : 22,
        '_ModifiedAttributeDict__overrides'           : 0,
        '_ModifiedAttributeDict__penalizedMultipliers': 0,
        '_ModifiedAttributeDict__postIncreases'       : 0,
        '_ModifiedAttributeDict__preAssigns'          : 0,
        '_ModifiedAttributeDict__preIncreases'        : 4,
    }

    # Test before calculating attributes
    for test_dict in rifter_modifier_dicts:
        assert len(getattr(RifterFit.ship.itemModifiedAttributes, test_dict)) == 0

    # Get base stats
    max_target_range_1 = RifterFit.ship.getModifiedItemAttr('maxTargetRange')
    scan_resolution_1 = RifterFit.ship.getModifiedItemAttr('scanResolution')

    RifterFit.clear()
    RifterFit.calculateModifiedAttributes()

    # Get self calculated stats
    max_target_range_2 = RifterFit.ship.getModifiedItemAttr('maxTargetRange')
    scan_resolution_2 = RifterFit.ship.getModifiedItemAttr('scanResolution')

    RifterFit.clear()
    # Project Heron fit onto Rifter
    RifterFit._Fit__projectedFits[HeronFit.ID] = HeronFit

    # DB['saveddata_session'].commit()
    # DB['saveddata_session'].flush()
    # DB['saveddata_session'].refresh(HeronFit)

    RifterFit.calculateModifiedAttributes()

    # Get stats with projections
    max_target_range_3 = RifterFit.ship.getModifiedItemAttr('maxTargetRange')
    scan_resolution_3 = RifterFit.ship.getModifiedItemAttr('scanResolution')

    RifterFit.clear()
    RifterFit.calculateModifiedAttributes()

    # Get stats with projections
    max_target_range_4 = RifterFit.ship.getModifiedItemAttr('maxTargetRange')
    scan_resolution_4 = RifterFit.ship.getModifiedItemAttr('scanResolution')

    RifterFit.clear()
    HeronFit.calculateModifiedAttributes(targetFit=RifterFit)
    RifterFit.calculateModifiedAttributes()

    # Get stats with projections
    max_target_range_5 = RifterFit.ship.getModifiedItemAttr('maxTargetRange')
    scan_resolution_5 = RifterFit.ship.getModifiedItemAttr('scanResolution')

    for test_dict in rifter_modifier_dicts:
        assert len(getattr(RifterFit.ship.itemModifiedAttributes, test_dict)) == rifter_modifier_dicts[test_dict]

