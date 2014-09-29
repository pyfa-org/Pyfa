# cpuNeedBonusEffectLasers
#
# Used by:
# Modules named like: Algid Energy Administrations Unit (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                  "cpu", module.getModifiedItemAttr("cpuNeedBonus"))