# shipSPTTrackingSpeedBonusRookie
#
# Used by:
# Ship: Echo
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("rookieSPTTracking"))
