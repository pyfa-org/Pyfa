# shipBonusMineralBayGI2
#
# Used by:
# Ship: Kryos
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("specialMineralHoldCapacity", ship.getModifiedItemAttr("shipBonusGI2"), skill="Gallente Industrial")
