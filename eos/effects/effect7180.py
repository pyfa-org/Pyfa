# miningDurationMultiplierOnline
#
# Used by:
# Module: Frostline 'Omnivore' Harvester Upgrade
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mining Laser",
                                  "duration", module.getModifiedItemAttr("miningDurationMultiplier"))
