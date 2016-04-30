# remoteSensorDampFalloff
#
# Used by:
# Modules from group: Sensor Dampener (6 of 6)
# Drones named like: SD (3 of 3)
type= "projected", "active"
def handler(fit, module, context):
    if "projected" not in context:
        return
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                           stackingPenalties = True)
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                           stackingPenalties = True)
