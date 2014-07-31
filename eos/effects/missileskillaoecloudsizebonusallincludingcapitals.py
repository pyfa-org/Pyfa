# Used by:
# Implants named like: Crash Booster (4 of 4)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "aoeCloudSize", implant.getModifiedItemAttr("aoeCloudSizeBonus"))
