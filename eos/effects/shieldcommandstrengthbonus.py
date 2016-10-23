type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
