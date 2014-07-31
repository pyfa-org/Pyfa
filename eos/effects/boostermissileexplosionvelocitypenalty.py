# Used by:
# Implants named like: Blue Pill Booster (3 of 5)
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "aoeVelocity", booster.getModifiedItemAttr("boosterAOEVelocityPenalty"))
