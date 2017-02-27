# shipBonusSupercarrierA5WarfareLinksBonus
#
# Used by:
# Ship: Aeon
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command") or mod.item.requiresSkill("Information Command"),
                                  attrs, src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
