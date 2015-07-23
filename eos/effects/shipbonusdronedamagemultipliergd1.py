# shipBonusDroneDamageMultiplierGD1
#
# Used by:
# Ship: Algos
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
