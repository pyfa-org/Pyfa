# shipHybridTrackingGC
#
# Used by:
# Ship: Lachesis
# Ship: Phobos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC") * level)
