# Used by:
# Ships from group: Black Ops (4 of 4)
# Ships from group: Blockade Runner (4 of 4)
# Ships from group: Covert Ops (5 of 5)
# Ships from group: Force Recon Ship (5 of 5)
# Ships from group: Stealth Bomber (4 of 4)
# Ships named like: Stratios (2 of 2)
# Subsystems named like: Offensive Covert Reconfiguration (4 of 4)
# Ship: Astero
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredItemForce(lambda mod: mod.item.group.name == "Cloaking Device",
                                  "moduleReactivationDelay", container.getModifiedItemAttr("covertOpsAndReconOpsCloakModuleDelay"))
