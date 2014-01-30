# Used by:
# Implant: Improved Crash Booster
# Implant: Standard Crash Booster
# Implant: Strong Crash Booster
# Implant: Synth Crash Booster
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "aoeCloudSize", implant.getModifiedItemAttr("aoeCloudSizeBonus"))
