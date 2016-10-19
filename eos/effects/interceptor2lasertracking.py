# interceptor2LaserTracking
#
# Used by:
# Ship: Crusader
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusInterceptor2"),
                                  skill="Interceptors")
