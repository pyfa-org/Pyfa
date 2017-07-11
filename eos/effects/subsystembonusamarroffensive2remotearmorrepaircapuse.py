# subsystemBonusAmarrOffensive2RemoteArmorRepairCapUse
#
# Used by:
# Subsystem: Legion Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                  src.getModifiedItemAttr("subsystemBonusAmarrOffensive2"), skill="Amarr Offensive Systems")
