# Used by:
# Ship: Anshar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Freighter").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusG1") * level)
