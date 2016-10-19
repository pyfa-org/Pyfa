# covertOpsCloakCpuPenalty
#
# Used by:
# Subsystems from group: Offensive Systems (12 of 16)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Cloaking"),
                                     "covertCloakCPUAdd", module.getModifiedItemAttr("covertCloakCPUPenalty"))
