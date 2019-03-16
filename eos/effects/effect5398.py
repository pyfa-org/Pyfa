# systemScanDurationModuleModifier
#
# Used by:
# Modules from group: Scanning Upgrade Time (2 of 2)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                  "duration", module.getModifiedItemAttr("scanDurationBonus"))
