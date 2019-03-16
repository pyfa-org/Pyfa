# shipArmorHitPointsAC1
#
# Used by:
# Ship: Monitor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("armorHP", src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
