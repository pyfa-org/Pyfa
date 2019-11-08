# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..', '..')))

import pytest
from eos.utils.stats import DmgTypes, RRTypes


@pytest.fixture()
def setup_damage_types():
    return DmgTypes(10, 20, 30, 40)


def test_dmgtypes_names():
    assert DmgTypes.Names() == ['em', 'thermal', 'kinetic', 'explosive']
    assert DmgTypes.Names(True) == ['em', 'th', 'kin', 'exp']
    assert DmgTypes.Names(short=True) == ['em', 'th', 'kin', 'exp']


def test_dmgtypes__repr(setup_damage_types):
    assert setup_damage_types.__repr__() == '<DmgTypes(em=10, thermal=20, kinetic=30, explosive=40, total=100)>'


def test_dmgtypes_names_lambda():
    assert DmgTypes.Names(False, lambda v: v.capitalize()) == ['Em', 'Thermal', 'Kinetic', 'Explosive']
    assert DmgTypes.Names(True, lambda v: v.upper()) == ['EM', 'TH', 'KIN', 'EXP']


@pytest.fixture()
def setup_rr_types():
    return RRTypes(10, 20, 30, 40)


def test_rrtypes_names():
    assert RRTypes.Names() == ['shield', 'armor', 'hull']
    assert RRTypes.Names(True) == ['shield', 'armor', 'hull']
    assert RRTypes.Names(ehpOnly=True) == ['shield', 'armor', 'hull']
    assert RRTypes.Names(False) == ['shield', 'armor', 'hull', 'capacitor']


def test_rrtypes__repr(setup_rr_types):
    assert setup_rr_types.__repr__() == '<RRTypes(shield=10, armor=20, hull=30, capacitor=40)>'


def test_rrtypes_names_lambda():
    assert RRTypes.Names(True, lambda v: v.capitalize()) == ['Shield', 'Armor', 'Hull']
    assert RRTypes.Names(postProcessor=lambda v: v.upper(), ehpOnly=False) == ['SHIELD', 'ARMOR', 'HULL', 'CAPACITOR']


