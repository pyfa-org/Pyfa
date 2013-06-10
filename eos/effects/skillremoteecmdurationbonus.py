# Used by:
# Skill: Projected Electronic Counter Measures
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote ECM Burst",
                                  "duration", skill.getModifiedItemAttr("projECMDurationBonus") * skill.level)
