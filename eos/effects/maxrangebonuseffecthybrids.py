# maxRangeBonusEffectHybrids
#
# Used by:
# Modules named like: Hybrid Locus Coordinator (8 of 8)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                  "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                  stackingPenalties=True)
