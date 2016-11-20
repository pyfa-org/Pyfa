# armoredSquadronCommand
#
# Used by:
# Skill: Armored Command Specialist
runTime = "early"
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command Specialist"),
                                  "commandBonus", skill.getModifiedItemAttr("squadronCommandBonus") * skill.level)
