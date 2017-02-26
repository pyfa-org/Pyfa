# eliteBonusCommandShipSiegeCS3
#
# Used by:
# Ships from group: Command Ship (4 of 8)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Value",
                                  src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Value",
                                  src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Value",
                                  src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                  src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Value",
                                  src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
