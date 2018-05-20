# Not used by any item
type = "passive"
runTime = "early"


def handler(fit, src, context):
    fit.ship.forceItemAttr("structureFullPowerStateHitpointMultiplier", src.getModifiedItemAttr("serviceModuleFullPowerStateHitpointMultiplier"))
