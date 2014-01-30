# Used by:
# Ships from group: Stealth Bomber (4 of 4)
# Subsystem: Legion Offensive - Covert Reconfiguration
# Subsystem: Loki Offensive - Covert Reconfiguration
# Subsystem: Proteus Offensive - Covert Reconfiguration
# Subsystem: Tengu Offensive - Covert Reconfiguration
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Cloaking Device",
                                     "cpu", container.getModifiedItemAttr("cloakingCpuNeedBonus"))
