# miningForemanStrengthBonus
#
# Used by:
# Skill: Mining Director
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Multiplier", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Multiplier", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Multiplier", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Multiplier", src.getModifiedItemAttr("commandStrengthBonus") * lvl)