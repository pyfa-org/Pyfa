# Used by:
# Implant: Improved Drop Booster
# Implant: Improved X-Instinct Booster
# Implant: Standard Drop Booster
# Implant: Standard X-Instinct Booster
# Implant: Strong Drop Booster
# Implant: Strong X-Instinct Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "falloff", booster.getModifiedItemAttr("boosterTurretFalloffPenalty"))
