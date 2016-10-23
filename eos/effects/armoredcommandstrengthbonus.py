type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
    fit.modules.filteredChargeBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Value", src.getModifiedItemAttr("commandStrengthBonus") * lvl)
