# shipHeatDamageMinmatarTacticalDestroyer3
#
# Used by:
# Ship: Svipul
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusTacticalDestroyerMinmatar3") * level)
