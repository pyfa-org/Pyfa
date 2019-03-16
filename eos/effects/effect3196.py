# thermodynamicsSkillDamageBonus
#
# Used by:
# Skill: Thermodynamics
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: "heatDamage" in mod.item.attributes, "heatDamage",
                                  skill.getModifiedItemAttr("thermodynamicsHeatDamage") * skill.level)
