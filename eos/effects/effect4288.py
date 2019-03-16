# subsystemBonusGallenteOffensive2RemoteArmorRepairCapUse
#
# Used by:
# Subsystem: Proteus Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                  src.getModifiedItemAttr("subsystemBonusGallenteOffensive2"), skill="Gallente Offensive Systems")
