# Used by:
# Implant: Improved Blue Pill Booster
# Implant: Standard Blue Pill Booster
# Implant: Strong Blue Pill Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "aoeVelocity", booster.getModifiedItemAttr("boosterAOEVelocityPenalty"))
