# shipHeatDamageAmarrTacticalDestroyer3
#
# Used by:
# Ship: Confessor
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusTacticalDestroyerAmarr3") * level)
