# subsystemBonusMinmatarDefensive2HardenerHeat
#
# Used by:
# Subsystem: Loki Defensive - Augmented Durability
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadSelfDurationBonus",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadHardeningBonus",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Tactical Shield Manipulation"), "overloadHardeningBonus",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")
