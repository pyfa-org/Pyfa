# skirmishCommandStrengthBonus
#
# Used by:
# Skill: Skirmish Command Specialist
type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Modifier", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Modifier", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Modifier", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Modifier", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
