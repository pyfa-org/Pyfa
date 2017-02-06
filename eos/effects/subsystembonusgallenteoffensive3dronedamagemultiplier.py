# subsystemBonusGallenteOffensive3DroneDamageMultiplier
#
# Used by:
# Subsystem: Proteus Offensive - Drone Synthesis Projector
type = "passive"


def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", module.getModifiedItemAttr("subsystemBonusGallenteOffensive3"),
                                 skill="Gallente Offensive Systems")
