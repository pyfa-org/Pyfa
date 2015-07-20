# shipHeatDamageGallenteTacticalDestroyer3
#
# Used by:
# Ship: Hecate
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusTacticalDestroyerGallente3"), skill="Gallente Tactical Destroyer")
