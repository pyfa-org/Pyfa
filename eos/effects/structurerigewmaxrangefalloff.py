# Not used by any item
type = "passive"


def handler(fit, src, context):
    groups = ("Structure ECM Battery", "Structure Disruption Battery")

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "falloff", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                  stackingPenalties=True)

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "maxRange", src.getModifiedItemAttr("structureRigEwarOptimalBonus"),
                                  stackingPenalties=True)

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "falloffEffectiveness", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                  stackingPenalties=True)
