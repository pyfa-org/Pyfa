# Used by:
# Ship: Rhea
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Freighter").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("freighterBonusC1") * level)
