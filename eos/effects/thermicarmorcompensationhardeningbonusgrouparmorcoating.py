# thermicArmorCompensationHardeningBonusGroupArmorCoating
#
# Used by:
# Skill: Thermal Armor Compensation
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Coating",
                                  "thermalDamageResistanceBonus", skill.getModifiedItemAttr("hardeningBonus") * skill.level)