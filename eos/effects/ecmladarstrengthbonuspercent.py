# Used by:
# Modules from group: ECM Stabilizer (6 of 6)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "scanLadarStrengthBonus", module.getModifiedItemAttr("ecmStrengthBonusPercent"),
                                  stackingPenalties = True)
