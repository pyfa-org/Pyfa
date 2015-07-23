# shipShieldThermalResistance1CBC2
#
# Used by:
# Variations of ship: Ferox (2 of 2)
# Ship: Drake
# Ship: Nighthawk
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")
