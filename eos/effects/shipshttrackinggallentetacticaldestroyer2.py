# shipSHTTrackingGallenteTacticalDestroyer2
#
# Used by:
# Ship: Hecate
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusTacticalDestroyerGallente2"), skill="Gallente Tactical Destroyer")
