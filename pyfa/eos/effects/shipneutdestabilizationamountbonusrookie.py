# shipNeutDestabilizationAmountBonusRookie
#
# Used by:
# Ship: Hematos
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Destabilizer",
                                  "energyDestabilizationAmount", ship.getModifiedItemAttr("rookieNeutDrain"))
