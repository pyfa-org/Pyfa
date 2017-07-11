# subsystemBonusMinmatarDefensive2LocalRepHeat
#
# Used by:
# Subsystem: Loki Defensive - Adaptive Defense Node
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Shield Operation"),
                                  "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"),
                                  skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "overloadArmorDamageAmount", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"),
                                  skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "overloadShieldBonus", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"),
                                  skill="Minmatar Defensive Systems")
