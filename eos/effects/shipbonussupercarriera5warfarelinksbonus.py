# shipBonusSupercarrierA5WarfareLinksBonus
#
# Used by:
# Ship: Aeon
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"), "warfareBuff4Value", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"), "warfareBuff3Value", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"), "buffDuration", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"), "warfareBuff2Value", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"), "warfareBuff1Value", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
