# shipBonusCargoMI
#
# Used by:
# Variations of ship: Wreathe (2 of 2)
# Ship: Mammoth
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Industrial").level
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipBonusMI") * level)
