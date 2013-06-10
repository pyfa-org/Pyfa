# Used by:
# Ship: Leviathan
type = "gang"
gangBoost = "shieldCapacity"
gangBonus = "shipBonusCT2"
def handler(fit, ship, context):
    fit.ship.boostItemAttr(gangBoost, ship.getModifiedItemAttr(gangBonus))
