# shipArmorThermalResistancePBC2
#
# Used by:
# Ship: Drekavac
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("shipBonusPBC2"),
                           skill="Precursor Battlecruiser")
