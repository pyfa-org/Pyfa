# miningSquadronCommand
#
# Used by:
# Skill: Mining Director
runTime = "early"
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Director"),
                                  "commandBonus", skill.getModifiedItemAttr("squadronCommandBonus") * skill.level)
