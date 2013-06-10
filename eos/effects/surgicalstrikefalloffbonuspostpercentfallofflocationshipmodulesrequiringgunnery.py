# Used by:
# Implants named like: Sooth Sayer Booster (4 of 4)
# Implants named like: Zainou 'Deadeye' Trajectory Analysis TA (6 of 6)
# Skill: Trajectory Analysis
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "falloff", container.getModifiedItemAttr("falloffBonus") * level)
