# shipVelocityBonusAI
#
# Used by:
# Variations of ship: Bestower (2 of 2)
# Ship: Prorator
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Industrial").level
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusAI") * level)
