# moduleBonusDroneNavigationComputer
#
# Used by:
# Modules from group: Drone Navigation Computer (8 of 8)
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity", src.getModifiedItemAttr("speedFactor"), stackingPenalties=True)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxVelocity", src.getModifiedItemAttr("speedFactor"), stackingPenalties=True)
