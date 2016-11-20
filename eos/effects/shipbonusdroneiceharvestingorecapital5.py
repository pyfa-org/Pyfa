# Ice Harvesting Drone Duration
#
# Used by:
# Orca
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Ice Harvesting Drone Operation"),
                                 "duration",
                                 src.getModifiedItemAttr("shipBonusORECapital5"),
                                 skill="Capital Industrial Ships"
                                 )

#  TODO: test
