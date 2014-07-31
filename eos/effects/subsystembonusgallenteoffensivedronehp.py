# Used by:
# Subsystem: Proteus Offensive - Drone Synthesis Projector
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Offensive Systems").level
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"), layer,
                                     module.getModifiedItemAttr("subsystemBonusGallenteOffensive") * level)
