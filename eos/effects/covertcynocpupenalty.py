# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Cynosural Field Theory"),
                                     "covertCloakCPUAdd", module.getModifiedItemAttr("covertCloakCPUPenalty"))
