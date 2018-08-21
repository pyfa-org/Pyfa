# structureHiddenArmorHPMultiplier
#
# Used by:
# Items from category: Structure (14 of 14)
type = "passive"


def handler(fit, src, context):
    fit.ship.multiplyItemAttr("armorHP", src.getModifiedItemAttr("hiddenArmorHPMultiplier") or 0)
