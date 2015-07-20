# shipBonusDroneDamageMultiplierAC2
#
# Used by:
# Variations of ship: Arbitrator (3 of 3)
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
