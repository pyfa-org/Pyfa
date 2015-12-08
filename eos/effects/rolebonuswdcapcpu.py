type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "cpu", src.getModifiedItemAttr("roleBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"), "capacitorNeed", src.getModifiedItemAttr("roleBonus"))
