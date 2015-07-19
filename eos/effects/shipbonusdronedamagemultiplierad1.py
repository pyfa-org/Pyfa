# shipBonusDroneDamageMultiplierAD1
#
# Used by:
# Ship: Dragoon
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
