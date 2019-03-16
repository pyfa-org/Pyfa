# fuelConservationCapNeedBonusPostPercentCapacitorNeedLocationShipModulesRequiringAfterburner
#
# Used by:
# Skill: Afterburner
# Skill: Fuel Conservation
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "capacitorNeed", skill.getModifiedItemAttr("capNeedBonus") * skill.level)
