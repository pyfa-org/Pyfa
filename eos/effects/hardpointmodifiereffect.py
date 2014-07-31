# Used by:
# Subsystems from group: Engineering Systems (16 of 16)
# Subsystems from group: Offensive Systems (16 of 16)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("turretSlotsLeft", module.getModifiedItemAttr("turretHardPointModifier"))
    fit.ship.increaseItemAttr("launcherSlotsLeft", module.getModifiedItemAttr("launcherHardPointModifier"))