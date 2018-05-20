# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.ship.multiplyItemAttr("armorHP", src.getModifiedItemAttr("hiddenArmorHPMultiplier") or 0)
