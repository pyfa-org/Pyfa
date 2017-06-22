type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "cpu", src.getModifiedItemAttr("subsystemMRSBFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "power", src.getModifiedItemAttr("subsystemMRSBFittingReduction"))
