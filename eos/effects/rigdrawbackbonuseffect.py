# Not used by any item
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill),
                                  "drawback", skill.getModifiedItemAttr("rigDrawbackBonus") * skill.level)
