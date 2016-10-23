# skirmishSquadronCommand
#
# Used by:
# Skill: Skirmish Command Specialist
runTime = "early"
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command Specialist"),
                                  "commandBonus", skill.getModifiedItemAttr("squadronCommandBonus") * skill.level)
