# Drone hitpoints, damage, and mining yield
#
# Used by:
# Orca
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier",
                                 src.getModifiedItemAttr("shipBonusORECapital4"),
                                 skill="Capital Industrial Ships"
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "shieldCapacity",
                                 src.getModifiedItemAttr("shipBonusORECapital4"),
                                 skill="Capital Industrial Ships"
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "armorHP",
                                 src.getModifiedItemAttr("shipBonusORECapital4"),
                                 skill="Capital Industrial Ships"
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "hp",
                                 src.getModifiedItemAttr("shipBonusORECapital4"),
                                 skill="Capital Industrial Ships"
                                 )

    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                 "miningAmount",
                                 src.getModifiedItemAttr("shipBonusORECapital4"),
                                 skill="Capital Industrial Ships"
                                 )

#  TODO: test
