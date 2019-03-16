# shipBonusDroneIceHarvestingORECapital5
#
# Used by:
# Ship: Rorqual
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Ice Harvesting Drone Operation"),
                                 "duration",
                                 src.getModifiedItemAttr("shipBonusORECapital5"),
                                 skill="Capital Industrial Ships"
                                 )
