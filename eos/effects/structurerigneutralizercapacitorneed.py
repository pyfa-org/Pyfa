type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                     "capacitorNeed", src.getModifiedItemAttr("structureRigEwarCapUseBonus"),
                                     stackingPenalties=True)
