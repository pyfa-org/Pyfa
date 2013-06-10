# Used by:
# Implants named like: Frentix Booster (4 of 4)
# Implants named like: Zainou 'Deadeye' Sharpshooter ST (6 of 6)
# Skill: Sharpshooter
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "maxRange", container.getModifiedItemAttr("rangeSkillBonus") * level)
