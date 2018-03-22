# missileLauncherSpeedMultiplier
#
# Used by:
# Modules from group: Ballistic Control system (20 of 20)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties=True)
