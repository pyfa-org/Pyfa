# capitalRemoteEnergyTransferCapNeedBonusSkill
#
# Used by:
# Skill: Capital Capacitor Emission Systems
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                  "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)