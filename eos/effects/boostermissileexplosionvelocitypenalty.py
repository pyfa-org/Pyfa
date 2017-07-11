# boosterMissileExplosionVelocityPenalty
#
# Used by:
# Implants named like: Blue Pill Booster (3 of 5)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Missile Explosion Velocity"

# Attribute that this effect targets
attr = "boosterAOEVelocityPenalty"


def handler(fit, booster, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "aoeVelocity", booster.getModifiedItemAttr(attr))
