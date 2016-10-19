# falloffBonusEffectLasers
#
# Used by:
# Modules named like: Energy Ambit Extension (8 of 8)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                  "falloff", module.getModifiedItemAttr("falloffBonus"),
                                  stackingPenalties=True)
