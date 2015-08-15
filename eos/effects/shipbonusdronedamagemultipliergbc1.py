# shipBonusDroneDamageMultiplierGBC1
#
# Used by:
# Variations of ship: Myrmidon (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusGBC1"), skill="Gallente Battlecruiser")
