# shipArmorThermalResistanceMC2
#
# Used by:
# Ship: Mimir
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("shipBonusMC2"),
                           skill="Minmatar Cruiser")
