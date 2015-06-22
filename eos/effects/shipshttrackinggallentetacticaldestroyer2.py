# shipSHTTrackingGallenteTacticalDestroyer2
#
# Used by:
# Ship: Hecate
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusTacticalDestroyerGallente2") * level)
