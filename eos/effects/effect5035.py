# shipBonusDroneHitpointsRookie
#
# Used by:
# Variations of ship: Procurer (2 of 2)
# Ship: Gnosis
# Ship: Praxis
# Ship: Sunesis
# Ship: Taipan
# Ship: Velator
type = "passive"


def handler(fit, ship, context):
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     type, ship.getModifiedItemAttr("rookieDroneBonus"))
