# shipBonusDroneMiningAmountRole
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                 "miningAmount",
                                 src.getModifiedItemAttr("roleBonusDroneMiningYield"),
                                 )

#  TODO: test
