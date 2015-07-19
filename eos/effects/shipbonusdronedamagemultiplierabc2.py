# shipBonusDroneDamageMultiplierABC2
#
# Used by:
# Ship: Prophecy
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusABC2"), skill="Amarr Battlecruiser")
