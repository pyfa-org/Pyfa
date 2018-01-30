# boosterTurretOptimalRangePenalty
#
# Used by:
# Implants named like: Blue Pill Booster (3 of 5)
# Implants named like: Mindflood Booster (3 of 4)
# Implants named like: Sooth Sayer Booster (3 of 4)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Turret Optimal Range"

# Attribute that this effect targets
attr = "boosterTurretOptimalRangePenalty"


def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "maxRange", booster.getModifiedItemAttr(attr))
