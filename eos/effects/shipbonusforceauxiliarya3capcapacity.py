# shipBonusForceAuxiliaryA3CapCapacity
#
# Used by:
# Ship: Apostle
type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("capacitorCapacity", src.getModifiedItemAttr("shipBonusForceAuxiliaryA3"), skill="Amarr Carrier")
