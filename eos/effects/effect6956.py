# subsystemRemoteArmorRepairerOptimalBonus
#
# Used by:
# Subsystems named like: Offensive Support Processor (3 of 4)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Remote Armor Repairer", "Ancillary Remote Armor Repairer"),
                                  "maxRange", src.getModifiedItemAttr("remoteArmorRepairerOptimalBonus"))
