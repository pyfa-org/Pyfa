# shipCargoBonusAI
#
# Used by:
# Variations of ship: Sigil (2 of 2)
# Ship: Bestower
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("shipBonusAI"), skill="Amarr Industrial")
