# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                  "maxRange", src.getModifiedItemAttr("structureRigEwarOptimalBonus"),
                                  stackingPenalties=True)

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                  "falloffEffectiveness", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                  stackingPenalties=True)
