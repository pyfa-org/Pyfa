# shipBonusDroneHPDamageMiningICS4
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier",
                                 src.getModifiedItemAttr("shipBonusICS4"),
                                 skill="Industrial Command Ships"
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "shieldCapacity",
                                 src.getModifiedItemAttr("shipBonusICS4"),
                                 skill="Industrial Command Ships"
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "armorHP",
                                 src.getModifiedItemAttr("shipBonusICS4"),
                                 skill="Industrial Command Ships"
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "hp",
                                 src.getModifiedItemAttr("shipBonusICS4"),
                                 skill="Industrial Command Ships"
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                 "miningAmount",
                                 src.getModifiedItemAttr("shipBonusICS4"),
                                 skill="Industrial Command Ships"
                                 )
