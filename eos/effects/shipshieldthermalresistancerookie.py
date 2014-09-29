# shipShieldThermalResistanceRookie
#
# Used by:
# Ship: Ibis
# Ship: Taipan
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))
