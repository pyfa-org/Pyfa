# Used by:
# Subsystem: Proteus Offensive - Drone Synthesis Projector
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Offensive Systems").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", module.getModifiedItemAttr("subsystemBonusGallenteOffensive3") * level)
