# covertOpsCpuBonus1
#
# Used by:
# Ships from group: Stealth Bomber (4 of 4)
# Subsystems named like: Offensive Covert Reconfiguration (4 of 4)
type = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Cloaking Device",
                                     "cpu", container.getModifiedItemAttr("cloakingCpuNeedBonus"))
