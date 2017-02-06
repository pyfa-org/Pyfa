# shipHeatDamageCaldariTacticalDestroyer3
#
# Used by:
# Ship: Jackdaw
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusTacticalDestroyerCaldari3"),
                                  skill="Caldari Tactical Destroyer")
