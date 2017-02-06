# interceptor2HybridTracking
#
# Used by:
# Ship: Taranis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusInterceptor2"),
                                  skill="Interceptors")
