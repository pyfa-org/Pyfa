# shipBonusDroneIceHarvestingRole
#
# Used by:
# Ship: Orca
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting Drone Operation"), "duration",
                                 src.getModifiedItemAttr("roleBonusDroneIceHarvestingSpeed"))
