# shipBonusDroneIceHarvestingICS5
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Ice Harvesting Drone Operation"),
                                 "duration",
                                 src.getModifiedItemAttr("shipBonusICS5"),
                                 skill="Industrial Command Ships"
                                 )

#  TODO: test
