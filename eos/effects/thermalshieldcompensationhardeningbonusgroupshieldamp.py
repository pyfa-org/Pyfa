# thermalShieldCompensationHardeningBonusGroupShieldAmp
#
# Used by:
# Skill: Thermal Shield Compensation
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Amplifier",
                                  "thermalDamageResistanceBonus", skill.getModifiedItemAttr("hardeningBonus") * skill.level)