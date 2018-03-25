# shipAgilityBonusGC1
#
# Used by:
# Ship: Monitor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")
