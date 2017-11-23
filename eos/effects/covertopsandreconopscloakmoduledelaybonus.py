# covertOpsAndReconOpsCloakModuleDelayBonus
#
# Used by:
# Ships from group: Black Ops (5 of 5)
# Ships from group: Blockade Runner (4 of 4)
# Ships from group: Covert Ops (7 of 7)
# Ships from group: Expedition Frigate (2 of 2)
# Ships from group: Force Recon Ship (7 of 8)
# Ships from group: Stealth Bomber (4 of 5)
# Ships named like: Stratios (2 of 2)
# Subsystems named like: Defensive Covert Reconfiguration (4 of 4)
# Ship: Astero
# Ship: Rabisu
type = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemForce(lambda mod: mod.item.requiresSkill("Cloaking"),
                                  "moduleReactivationDelay",
                                  container.getModifiedItemAttr("covertOpsAndReconOpsCloakModuleDelay"))
