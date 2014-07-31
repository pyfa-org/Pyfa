# Used by:
# Skill: Warfare Link Specialist
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Gang Coordinator",
                                  "commandBonusHidden", skill.getModifiedItemAttr("squadronCommandBonus") * skill.level)
