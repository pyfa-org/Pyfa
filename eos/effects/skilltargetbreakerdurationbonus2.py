# Used by:
# Skill: Target Breaker Amplification
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Breaker",
                                  "duration", skill.getModifiedItemAttr("durationBonus") * skill.level)
