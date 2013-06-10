# Used by:
# Modules from group: Signal Amplifier (11 of 11)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("maxLockedTargets", module.getModifiedItemAttr("maxLockedTargetsBonus"))
