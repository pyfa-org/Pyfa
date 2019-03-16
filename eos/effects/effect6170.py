# entosisCPUPenalty
#
# Used by:
# Ships from group: Interceptor (10 of 10)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Infomorph Psychology"),
                                     "entosisCPUAdd", ship.getModifiedItemAttr("entosisCPUPenalty"))
