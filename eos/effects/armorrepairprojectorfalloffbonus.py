type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer", "falloffEffectiveness", src.getModifiedItemAttr("falloffBonus"))
