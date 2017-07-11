# covertOpsCloakCpuPenalty
#
# Used by:
# Subsystems from group: Defensive Systems (8 of 12)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Cloaking"),
                                     "covertCloakCPUAdd", module.getModifiedItemAttr("covertCloakCPUPenalty"))
