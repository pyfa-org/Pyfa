# serviceModuleFullPowerHitpointPostAssign
#
# Used by:
# Structure Modules from group: Structure Citadel Service Module (2 of 2)
# Structure Modules from group: Structure Engineering Service Module (6 of 6)
# Structure Modules from group: Structure Resource Processing Service Module (4 of 4)
# Structure Module: Standup Moon Drill I
type = "passive"
runTime = "early"


def handler(fit, src, context):
    fit.ship.forceItemAttr("structureFullPowerStateHitpointMultiplier", src.getModifiedItemAttr("serviceModuleFullPowerStateHitpointMultiplier"))
