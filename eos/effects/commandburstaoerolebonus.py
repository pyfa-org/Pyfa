type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "maxRange", src.getModifiedItemAttr("roleBonusCommandBurstAoERange"), stackingPenalties=True)
