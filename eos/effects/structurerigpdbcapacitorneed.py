type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Structure Area Denial Module",
                                     "capacitorNeed", src.getModifiedItemAttr("structureRigPDCapUseBonus"),
                                     stackingPenalties=True)
