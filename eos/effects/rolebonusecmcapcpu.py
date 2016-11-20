# roleBonusECMCapCPU
#
# Used by:
# Ship: Griffin Navy Issue
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "capacitorNeed",
                                  src.getModifiedItemAttr("roleBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "cpu", src.getModifiedItemAttr("roleBonus"))
