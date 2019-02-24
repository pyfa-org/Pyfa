# structureHiddenArmorHPMultiplier
#
# Used by:
# Items from category: Structure (17 of 17)
type = "passive"


def handler(fit, src, context):
    fit.ship.multiplyItemAttr("armorHP", src.getModifiedItemAttr("hiddenArmorHPMultiplier") or 0)
