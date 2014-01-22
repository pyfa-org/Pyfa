# Used by:
# Implants named like: Trajectory TA (6 of 6)
# Implant: Improved Sooth Sayer Booster
# Implant: Standard Sooth Sayer Booster
# Implant: Strong Sooth Sayer Booster
# Implant: Synth Sooth Sayer Booster
# Skill: Trajectory Analysis
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "falloff", container.getModifiedItemAttr("falloffBonus") * level)
