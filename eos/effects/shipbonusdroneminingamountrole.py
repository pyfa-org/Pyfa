# Drone hitpoints, damage, and mining yield
#
# Used by:
# Orca
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                 "miningAmount",
                                 src.getModifiedItemAttr("roleBonusDroneMiningYield"),
                                 )

#  TODO: test
