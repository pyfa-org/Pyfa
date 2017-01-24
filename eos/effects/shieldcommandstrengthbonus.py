# shieldCommandStrengthBonus
#
# Used by:
# Skill: Shield Command Specialist
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Multiplier",
                                    src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Multiplier",
                                    src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Multiplier",
                                    src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Multiplier",
                                    src.getModifiedItemAttr("commandStrengthBonus") * lvl)
