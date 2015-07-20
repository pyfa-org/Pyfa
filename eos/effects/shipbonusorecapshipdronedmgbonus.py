# shipBonusORECapShipDroneDmgBonus
#
# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusORECapital4"), skill="Capital Industrial Ships")
