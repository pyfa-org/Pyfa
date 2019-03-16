# subsystemBonusAmarrDefensiveArmorRepairAmount
#
# Used by:
# Subsystem: Legion Defensive - Covert Reconfiguration
# Subsystem: Legion Defensive - Nanobot Injector
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                                  skill="Amarr Defensive Systems")
