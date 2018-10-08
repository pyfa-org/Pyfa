type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"), "damageMultiplierBonusPerCycle",
                                     src.getModifiedItemAttr("eliteBonusCovertOps3"), skill="Covert Ops")
