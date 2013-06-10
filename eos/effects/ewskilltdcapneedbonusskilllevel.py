# Used by:
# Implants named like: Zainou 'Gypsy' Weapon Disruption WD (6 of 6)
# Skill: Weapon Disruption
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
