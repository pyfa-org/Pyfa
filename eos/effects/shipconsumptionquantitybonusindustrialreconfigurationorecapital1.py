# shipConsumptionQuantityBonusIndustrialReconfigurationORECapital1
#
# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Industrial Reconfiguration"),
                                  "consumptionQuantity", ship.getModifiedItemAttr("shipBonusORECapital1"), skill="Capital Industrial Ships")
