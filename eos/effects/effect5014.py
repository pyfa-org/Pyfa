# shipBonusDroneDamageMultiplierRookie
#
# Used by:
# Ship: Gnosis
# Ship: Praxis
# Ship: Sunesis
# Ship: Taipan
# Ship: Velator
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("rookieDroneBonus"))
