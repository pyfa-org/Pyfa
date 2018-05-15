# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))

from service.attribute import Attribute


def test_attribute():
    """
    We don't really have much to test here, so throw a generic attribute at it and validate we get the expected results

    :return:
    """
    sAttr = Attribute.getInstance()
    info = sAttr.getAttributeInfo("maxRange")

    assert info.attributeID == 54
    assert type(info.attributeID) is int
    assert info.attributeName == 'maxRange'
    assert type(info.attributeName) is str
    assert info.defaultValue == 0.0
    assert type(info.defaultValue) is float
    assert info.description == 'Distance below which range does not affect the to-hit equation.'
    assert type(info.description) is str
    assert info.displayName == 'Optimal Range'
    assert type(info.displayName) is str
    assert info.highIsGood is True
    assert type(info.highIsGood) is bool
    assert info.iconID == 1391
    assert type(info.iconID) is int
    assert info.name == 'maxRange'
    assert type(info.name) is str
    assert info.published is True
    assert type(info.published) is bool
    assert info.unitID == 1
    assert type(info.unitID) is int
    assert info.unit.ID == 1
    assert type(info.unit.ID) is int
    assert info.unit.displayName == 'm'
    assert type(info.unit.displayName) is str
    assert info.unit.name == 'Length'
    assert type(info.unit.name) is str
    assert info.unit.unitID == 1
    assert type(info.unit.unitID) is int
    assert info.unit.unitName == 'Length'
    assert type(info.unit.unitName) is str
