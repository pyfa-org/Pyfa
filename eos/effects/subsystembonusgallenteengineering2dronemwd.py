# Used by:
# Subsystem: Proteus Engineering - Augmented Capacitor Reservoir
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Engineering Systems").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"), "maxVelocity",
                                 module.getModifiedItemAttr("subsystemBonusGallenteEngineering2") * level)
