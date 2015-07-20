# subsystemBonusAmarrOffensive3DroneHP
#
# Used by:
# Subsystem: Legion Offensive - Drone Synthesis Projector
type = "passive"
def handler(fit, module, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"), layer,
                                     module.getModifiedItemAttr("subsystemBonusAmarrOffensive3"), skill="Amarr Offensive Systems")
