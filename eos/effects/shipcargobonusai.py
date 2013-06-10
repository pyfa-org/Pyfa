# Used by:
# Variations of ship: Bestower (2 of 2)
# Variations of ship: Sigil (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Industrial").level
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipBonusAI") * level)
