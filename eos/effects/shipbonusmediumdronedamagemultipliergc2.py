# shipBonusMediumDroneDamageMultiplierGC2
#
# Used by:
# Ship: Ishtar
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
