# shipHeatDamageGallenteTacticalDestroyer3
#
# Used by:
# Ship: Hecate
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusTacticalDestroyerGallente3") * level)
