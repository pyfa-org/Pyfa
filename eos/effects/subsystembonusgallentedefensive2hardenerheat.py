# subsystemBonusGallenteDefensive2HardenerHeat
#
# Used by:
# Subsystem: Proteus Defensive - Augmented Plating
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadHardeningBonus",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive2"), skill="Gallente Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "overloadSelfDurationBonus",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive2"), skill="Gallente Defensive Systems")
