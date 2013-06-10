# Used by:
# Ship: Providence
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Freighter").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusA1") * level)
