type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                     "maxRange", src.getModifiedItemAttr("structureRigEwarOptimalBonus"),
                                     stackingPenalties=True)

    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                 "falloffEffectiveness", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                 stackingPenalties=True)
