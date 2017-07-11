# boosterTurretTrackingPenalty
#
# Used by:
# Implants named like: Exile Booster (3 of 4)
# Implants named like: Frentix Booster (3 of 4)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Turret Tracking"

# Attribute that this effect targets
attr = "boosterTurretTrackingPenalty"


def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "trackingSpeed", booster.getModifiedItemAttr(attr))
