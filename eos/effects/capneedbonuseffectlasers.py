# capNeedBonusEffectLasers
#
# Used by:
# Modules named like: Energy Discharge Elutriation (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                  "capacitorNeed", module.getModifiedItemAttr("capNeedBonus"))
