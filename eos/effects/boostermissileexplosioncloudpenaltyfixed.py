# Used by:
# Implant: Improved Exile Booster
# Implant: Improved Mindflood Booster
# Implant: Standard Exile Booster
# Implant: Standard Mindflood Booster
# Implant: Strong Exile Booster
# Implant: Strong Mindflood Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "aoeCloudSize", booster.getModifiedItemAttr("boosterMissileAOECloudPenalty"))
