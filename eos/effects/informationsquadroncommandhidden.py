# informationSquadronCommandHidden
#
# Used by:
# Skill: Information Command Specialist
runTime = "early"
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command Specialist"),
                                  "commandBonusHidden", skill.getModifiedItemAttr("squadronCommandBonus") * skill.level)
