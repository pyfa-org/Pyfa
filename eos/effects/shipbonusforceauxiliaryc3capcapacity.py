# shipBonusForceAuxiliaryC3CapCapacity
#
# Used by:
# Ship: Minokawa
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("capacitorCapacity", src.getModifiedItemAttr("shipBonusForceAuxiliaryC3"),
                           skill="Caldari Carrier")
