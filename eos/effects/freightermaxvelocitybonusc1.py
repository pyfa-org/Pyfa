# Used by:
# Ship: Charon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Freighter").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusC1") * level)
