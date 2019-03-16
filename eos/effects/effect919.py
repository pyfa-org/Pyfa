# shipHybridTrackingGC2
#
# Used by:
# Ship: Enforcer
# Ship: Thorax
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
