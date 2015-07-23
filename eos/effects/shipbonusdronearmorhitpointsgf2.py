# shipBonusDroneArmorHitpointsGF2
#
# Used by:
# Ship: Ishkur
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "armorHP", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
