# shipBonusAgilityAI2
#
# Used by:
# Ship: Sigil
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Industrial").level
    fit.ship.boostItemAttr("agility", ship.getModifiedItemAttr("shipBonusAI2") * level)
