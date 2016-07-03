runTime = "early"
type = "passive"
def handler(fit, src, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Cybernetics"),
                                             "armorRepairBonus", src.getModifiedItemAttr("implantSetSerpentis2"))
