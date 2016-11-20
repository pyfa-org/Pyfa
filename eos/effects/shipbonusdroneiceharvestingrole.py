# shipBonusDroneIceHarvestingRole
#
# Used by:
# Ship: Orca
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Ice Harvesting Drone Operation"), "duration", src.getModifiedItemAttr("roleBonusDroneIceHarvestingSpeed"))
