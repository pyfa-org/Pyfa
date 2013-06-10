# Used by:
# Ship: Nomad
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Freighter").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusM1") * level)
