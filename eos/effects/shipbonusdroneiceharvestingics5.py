# Ice Harvesting Drone Duration
#
# Used by:
# Orca
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Ice Harvesting Drone Operation"),
                                 "duration",
                                 src.getModifiedItemAttr("shipBonusICS5"),
                                 skill="Industrial Command Ships"
                                 )

#  TODO: test
