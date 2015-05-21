# shipHeatDamageCaldariTacticalDestroyer3
#
# Used by:
# Ship: Jackdaw
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusTacticalDestroyerCaldari3") * level)
