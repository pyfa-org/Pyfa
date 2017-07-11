# subsystemBonusAmarrDefensive3ArmorRepHeat
#
# Used by:
# Subsystem: Legion Defensive - Covert Reconfiguration
# Subsystem: Legion Defensive - Nanobot Injector
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusAmarrDefensive3"),
                                  skill="Amarr Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "overloadArmorDamageAmount", src.getModifiedItemAttr("subsystemBonusAmarrDefensive3"),
                                  skill="Amarr Defensive Systems")
