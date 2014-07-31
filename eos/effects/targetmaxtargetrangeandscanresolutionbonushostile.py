# Used by:
# Modules from group: Remote Sensor Damper (9 of 9)
type= "projected", "active"
def handler(fit, module, context):
    if "projected" not in context:
        return
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                           stackingPenalties = True)
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                           stackingPenalties = True)
