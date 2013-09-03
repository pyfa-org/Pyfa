# Used by:
# Skill: Skirmish Warfare Specialist
runTime = "early"
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Warfare Specialist"),
                                  "commandBonus", skill.getModifiedItemAttr("squadronCommandBonus") * skill.level)
