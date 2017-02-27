# shipBonusSupercarrierM5WarfareLinksBonus
#
# Used by:
# Ship: Hel
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command") or mod.item.requiresSkill("Shield Command"),
                                  attrs, src.getModifiedItemAttr("shipBonusSupercarrierM5"), skill="Minmatar Carrier")
