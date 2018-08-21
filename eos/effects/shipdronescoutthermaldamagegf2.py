# shipDroneScoutThermalDamageGF2
#
# Used by:
# Ship: Helios
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Light Drone Operation"),
                                 "thermalDamage", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
