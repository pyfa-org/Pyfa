# subsystemBonusGallenteEngineeringDroneHP
#
# Used by:
# Subsystem: Proteus Engineering - Augmented Capacitor Reservoir
type = "passive"


def handler(fit, module, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"), layer,
                                     module.getModifiedItemAttr("subsystemBonusGallenteEngineering"),
                                     skill="Gallente Engineering Systems")
