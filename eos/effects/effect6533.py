# shipBonusForceAuxiliaryA4WarfareLinksBonus
#
# Used by:
# Ship: Apostle
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                              mod.item.requiresSkill("Information Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                              mod.item.requiresSkill("Information Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                              mod.item.requiresSkill("Information Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                              mod.item.requiresSkill("Information Command"),
                                  "buffDuration", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or
                                              mod.item.requiresSkill("Information Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
