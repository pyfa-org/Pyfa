# shipSETTrackingBonusRookie
#
# Used by:
# Ship: Immolator
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("rookieSETTracking"))
