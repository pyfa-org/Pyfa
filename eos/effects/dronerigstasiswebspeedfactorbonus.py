# Used by:
# Modules named like: Stasis Drone Augmentor (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Stasis Webifying Drone",
                                 "speedFactor", module.getModifiedItemAttr("webSpeedFactorBonus"))