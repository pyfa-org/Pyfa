# subsystemBonusGallenteOffensiveDroneHP
#
# Used by:
# Subsystem: Proteus Offensive - Drone Synthesis Projector
type = "passive"


def handler(fit, module, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"), layer,
                                     module.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                     skill="Gallente Offensive Systems")
