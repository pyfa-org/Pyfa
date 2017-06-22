type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"), "cpu", src.getModifiedItemAttr("subsystemMHTFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"), "power", src.getModifiedItemAttr("subsystemMHTFittingReduction"))
