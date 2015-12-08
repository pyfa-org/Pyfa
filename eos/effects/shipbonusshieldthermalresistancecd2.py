# shipBonusShieldThermalResistanceCD2
#
# Used by:
# Ship: Stork
type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusCD2"), skill="Caldari Destroyer")
