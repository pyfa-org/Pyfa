# eliteBonusCommandShipSkirmishCS3
#
# Used by:
# Ships from group: Command Ship (4 of 8)
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff2Value", src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff1Value", src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff3Value", src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "warfareBuff4Value", src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), "buffDuration", src.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
