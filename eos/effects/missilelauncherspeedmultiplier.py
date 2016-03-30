# missileLauncherSpeedMultiplier
#
# Used by:
# Modules from group: Ballistic Control system (17 of 17)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties = True)
