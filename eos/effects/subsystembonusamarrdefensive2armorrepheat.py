# subsystemBonusAmarrDefensive2ArmorRepHeat
#
# Used by:
# Subsystem: Legion Defensive - Nanobot Injector
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"), "overloadArmorDamageAmount",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive2"), skill="Amarr Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"), "overloadSelfDurationBonus",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive2"), skill="Amarr Defensive Systems")
