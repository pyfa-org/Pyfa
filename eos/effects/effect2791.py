# boosterMissileExplosionCloudPenaltyFixed
#
# Used by:
# Implants named like: Exile Booster (3 of 4)
# Implants named like: Mindflood Booster (3 of 4)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Missile Explosion Radius"

# Attribute that this effect targets
attr = "boosterMissileAOECloudPenalty"


def handler(fit, booster, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "aoeCloudSize", booster.getModifiedItemAttr(attr))
