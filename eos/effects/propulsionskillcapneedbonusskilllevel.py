# propulsionSkillCapNeedBonusSkillLevel
#
# Used by:
# Implants named like: Zainou 'Gypsy' Propulsion Jamming PJ (6 of 6)
# Skill: Propulsion Jamming
type = "passive"


def handler(fit, container, context):

    level = container.level if "skill" in context else 1

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Propulsion Jamming"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
