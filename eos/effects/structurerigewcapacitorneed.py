type = "passive"
def handler(fit, src, context):
    groups = ("Structure ECM Battery", "Structure Disruption Battery")
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name in groups,
                                     "capacitorNeed", src.getModifiedItemAttr("structureRigEwarCapUseBonus"),
                                     stackingPenalties=True)