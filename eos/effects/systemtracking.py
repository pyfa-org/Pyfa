# Used by:
# Celestials named like: Magnetar Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gunnery"),
                                     "trackingSpeed", module.getModifiedItemAttr("trackingSpeedMultiplier"))
