# droneDurabilityShieldCapBonus
#
# Used by:
# Modules named like: Drone Durability Enhancer (6 of 8)
type = "passive"
def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                  "shieldCapacity", module.getModifiedItemAttr("hullHpBonus"))
