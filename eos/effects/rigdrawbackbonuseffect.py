# Used by:
# Skills named like: Rigging (9 of 10)
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill),
                                  "drawback", skill.getModifiedItemAttr("rigDrawbackBonus") * skill.level)
    