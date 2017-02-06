# informationCommandStrengthBonus
#
# Used by:
# Skill: Information Command Specialist
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff2Multiplier",
                                    src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff1Multiplier",
                                    src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff3Multiplier",
                                    src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Information Command"), "warfareBuff4Multiplier",
                                    src.getModifiedItemAttr("commandStrengthBonus") * lvl)
