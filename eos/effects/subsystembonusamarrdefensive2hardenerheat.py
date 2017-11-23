# subsystemBonusAmarrDefensive2HardenerHeat
#
# Used by:
# Subsystem: Legion Defensive - Augmented Plating
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadSelfDurationBonus",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive2"), skill="Amarr Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadHardeningBonus",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive2"), skill="Amarr Defensive Systems")
