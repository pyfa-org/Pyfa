# shipBonusForceAuxiliaryG4WarfareLinksBonus
#
# Used by:
# Ship: Ninazu
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Armored Command"),
                                  attrs, src.getModifiedItemAttr("shipBonusForceAuxiliaryG4"), skill="Gallente Carrier")
