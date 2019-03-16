# eliteIndustrialArmorRepairHeatBonus
#
# Used by:
# Ships from group: Deep Space Transport (4 of 4)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "overloadArmorDamageAmount", ship.getModifiedItemAttr("roleBonusOverheatDST"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "overloadSelfDurationBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))
