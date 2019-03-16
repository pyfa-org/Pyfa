# subsystemBonusGallenteDefensiveArmorRepairAmount
#
# Used by:
# Subsystem: Proteus Defensive - Covert Reconfiguration
# Subsystem: Proteus Defensive - Nanobot Injector
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusGallenteDefensive"),
                                  skill="Gallente Defensive Systems")
