# subsystemBonusMinmatarDefensiveShieldArmorRepairAmount
#
# Used by:
# Subsystem: Loki Defensive - Adaptive Defense Node
# Subsystem: Loki Defensive - Covert Reconfiguration
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                  skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                                  skill="Minmatar Defensive Systems")
