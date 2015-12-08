# shipNOSTransferAmountBonusRookie
#
# Used by:
# Ship: Hematos
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferAmount", ship.getModifiedItemAttr("rookieNosDrain"))
