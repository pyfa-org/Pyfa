# Used by:
# Skill: Thermodynamics
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  skill.getModifiedItemAttr("thermodynamicsHeatDamage") * skill.level)
