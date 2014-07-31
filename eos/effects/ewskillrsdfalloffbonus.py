# Used by:
# Skill: Frequency Modulation
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Sensor Linking"),
                                  "falloff", skill.getModifiedItemAttr("falloffBonus") * skill.level)
