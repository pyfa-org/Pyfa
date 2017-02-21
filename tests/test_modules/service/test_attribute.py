from service.attribute import Attribute

def test_attribute():
    """
    We don't really have much to test here, to throw a generic attribute at it and validate we get the expected results

    :return:
    """
    sAttr = Attribute.getInstance()
    info = sAttr.getAttributeInfo("maxRange")

    assert info.attributeID == 54
    assert type(info.attributeID) is int
    assert info.attributeName == 'maxRange'
    assert type(info.attributeName) is unicode
    assert info.defaultValue == 0.0
    assert type(info.defaultValue) is float
    assert info.description == 'Distance below which range does not affect the to-hit equation.'
    assert type(info.description) is unicode
    assert info.displayName == 'Optimal Range'
    assert type(info.displayName) is unicode
    assert info.highIsGood == True
    assert type(info.highIsGood) is bool
    assert info.iconID == 1391
    assert type(info.iconID) is int
    assert info.name == 'maxRange'
    assert type(info.name) is unicode
    assert info.published == True
    assert type(info.published) is bool
    assert info.unitID == 1
    assert type(info.unitID) is int
    assert info.unit.ID == 1
    assert type(info.unit.ID) is int
    assert info.unit.displayName == 'm'
    assert type(info.unit.displayName) is unicode
    assert info.unit.name == 'Length'
    assert type(info.unit.name) is unicode
    assert info.unit.unitID == 1
    assert type(info.unit.unitID) is int
    assert info.unit.unitName == 'Length'
    assert type(info.unit.unitName) is unicode
