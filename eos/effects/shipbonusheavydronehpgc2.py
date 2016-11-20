# shipBonusHeavyDroneHPGC2
#
# Used by:
# Ship: Ishtar
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                 "hp", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
