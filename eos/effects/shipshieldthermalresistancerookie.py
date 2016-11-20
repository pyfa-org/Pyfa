# shipShieldThermalResistanceRookie
#
# Used by:
# Ships from group: Heavy Interdiction Cruiser (3 of 5)
# Ship: Ibis
# Ship: Taipan
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", ship.getModifiedItemAttr("rookieShieldResistBonus"))
