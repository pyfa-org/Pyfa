# hardPointModifierEffect
#
# Used by:
# Subsystems from group: Offensive Systems (12 of 12)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("turretSlotsLeft", module.getModifiedItemAttr("turretHardPointModifier"))
    fit.ship.increaseItemAttr("launcherSlotsLeft", module.getModifiedItemAttr("launcherHardPointModifier"))
