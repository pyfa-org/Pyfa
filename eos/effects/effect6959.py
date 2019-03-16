# subsystemBonusGallenteOffensive3RemoteArmorRepairHeat
#
# Used by:
# Subsystem: Proteus Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "overloadSelfDurationBonus",
                                  src.getModifiedItemAttr("subsystemBonusGallenteOffensive3"), skill="Gallente Offensive Systems")
