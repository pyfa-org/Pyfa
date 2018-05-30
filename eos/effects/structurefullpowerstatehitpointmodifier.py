# structureFullPowerStateHitpointModifier
#
# Used by:
# Items from category: Structure (14 of 14)
type = "passive"


def handler(fit, src, context):
    fit.ship.multiplyItemAttr("shieldCapacity", src.getModifiedItemAttr("structureFullPowerStateHitpointMultiplier") or 0)
    fit.ship.multiplyItemAttr("armorHP", src.getModifiedItemAttr("structureFullPowerStateHitpointMultiplier") or 0)
