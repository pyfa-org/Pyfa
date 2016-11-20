# informationSquadronCommand
#
# Used by:
# Skill: Information Warfare Specialist
runTime = "early"
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"),
                                  "commandBonus", skill.getModifiedItemAttr("squadronCommandBonus") * skill.level)
