# eliteBonusCommandShipSkirmishCS3
#
# Used by:
# Ships from group: Command Ship (4 of 8)
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), attrs,
                                  src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
