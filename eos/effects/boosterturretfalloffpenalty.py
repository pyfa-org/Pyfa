# boosterTurretFalloffPenalty
#
# Used by:
# Implants named like: Drop Booster (3 of 4)
# Implants named like: X Instinct Booster (3 of 4)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Turret Falloff"

# Attribute that this effect targets
attr = "boosterTurretFalloffPenalty"


def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "falloff", booster.getModifiedItemAttr(attr))
