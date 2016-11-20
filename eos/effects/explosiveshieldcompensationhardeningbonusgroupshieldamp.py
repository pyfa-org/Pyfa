# explosiveShieldCompensationHardeningBonusGroupShieldAmp
#
# Used by:
# Skill: Explosive Shield Compensation
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Resistance Amplifier",
                                  "explosiveDamageResistanceBonus",
                                  skill.getModifiedItemAttr("hardeningBonus") * skill.level)
