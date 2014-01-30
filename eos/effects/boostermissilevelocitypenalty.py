# Used by:
# Implant: Improved Crash Booster
# Implant: Improved X-Instinct Booster
# Implant: Standard Crash Booster
# Implant: Standard X-Instinct Booster
# Implant: Strong Crash Booster
# Implant: Strong X-Instinct Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", "boosterMissileVelocityPenalty")
