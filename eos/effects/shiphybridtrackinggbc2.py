# shipHybridTrackingGBC2
#
# Used by:
# Ship: Brutix Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGBC2"), skill="Gallente Battlecruiser")
