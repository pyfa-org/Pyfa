# drawbackCPUNeedLaunchers
#
# Used by:
# Modules from group: Rig Launcher (48 of 48)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "cpu", module.getModifiedItemAttr("drawback"))
