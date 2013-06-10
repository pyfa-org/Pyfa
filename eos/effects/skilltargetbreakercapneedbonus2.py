# Used by:
# Skill: Target Breaker Amplification
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Breaker",
                                  "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)
