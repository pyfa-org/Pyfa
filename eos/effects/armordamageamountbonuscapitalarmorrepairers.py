# armorDamageAmountBonusCapitalArmorRepairers
#
# Used by:
# Modules named like: Auxiliary Nano Pump (8 of 8)
type = "passive"


def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                  "armorDamageAmount", implant.getModifiedItemAttr("repairBonus"),
                                  stackingPenalties=True)
