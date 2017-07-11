# subsystemBonusAmarrOffensive3RemoteArmorRepairHeat
#
# Used by:
# Subsystem: Legion Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "overloadSelfDurationBonus",
                                  src.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
