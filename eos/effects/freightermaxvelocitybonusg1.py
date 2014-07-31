# Used by:
# Ship: Obelisk
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Freighter").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusG1") * level)
