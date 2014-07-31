# Used by:
# Variations of ship: Fenrir (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Freighter").level
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusM2") * level)
