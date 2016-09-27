type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"), "capacitorNeed", src.getModifiedItemAttr("miningDurationRoleBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"), "duration", src.getModifiedItemAttr("miningDurationRoleBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"), "duration", src.getModifiedItemAttr("miningDurationRoleBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting"), "capacitorNeed", src.getModifiedItemAttr("miningDurationRoleBonus"))
