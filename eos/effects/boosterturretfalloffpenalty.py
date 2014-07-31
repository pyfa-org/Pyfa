# Used by:
# Implants named like: Drop Booster (3 of 4)
# Implants named like: X Instinct Booster (3 of 4)
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "falloff", booster.getModifiedItemAttr("boosterTurretFalloffPenalty"))
