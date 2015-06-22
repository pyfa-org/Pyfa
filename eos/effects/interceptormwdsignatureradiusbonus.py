# interceptorMWDSignatureRadiusBonus
#
# Used by:
# Ships from group: Interceptor (9 of 10)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interceptors").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusInterceptor") * level)
