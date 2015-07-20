# interceptorMWDSignatureRadiusBonus
#
# Used by:
# Ships from group: Interceptor (9 of 10)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusInterceptor"), skill="Interceptors")
