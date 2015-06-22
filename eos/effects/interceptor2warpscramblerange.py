# Interceptor2WarpScrambleRange
#
# Used by:
# Ships from group: Interceptor (5 of 10)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interceptors").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusInterceptor2") * level)