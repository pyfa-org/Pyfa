# Used by:
# Implants named like: Zainou 'Gypsy' Sensor Linking SL (6 of 6)
# Skill: Sensor Linking
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Sensor Linking"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
