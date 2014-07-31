# Used by:
# Ships from group: Capital Industrial Ship (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Capital Industrial Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Industrial Reconfiguration"),
                                  "consumptionQuantity", ship.getModifiedItemAttr("shipBonusORECapital1") * level)
