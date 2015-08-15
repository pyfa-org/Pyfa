# shipShieldKineticResistanceCC2
#
# Used by:
# Variations of ship: Moa (3 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldKineticDamageResonance", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
