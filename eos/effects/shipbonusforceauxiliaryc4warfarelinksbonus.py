# shipBonusForceAuxiliaryC4WarfareLinksBonus
#
# Used by:
# Ship: Minokawa
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"), "warfareBuff3Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"), "warfareBuff4Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"), "warfareBuff2Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"), "buffDuration", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command") or mod.item.requiresSkill("Information Command"), "warfareBuff1Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
