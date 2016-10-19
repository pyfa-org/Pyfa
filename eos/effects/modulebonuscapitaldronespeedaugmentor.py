# moduleBonusCapitalDroneSpeedAugmentor
#
# Used by:
# Variations of module: Capital Drone Speed Augmentor I (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxVelocity",
                                 src.getModifiedItemAttr("droneMaxVelocityBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                   src.getModifiedItemAttr("droneMaxVelocityBonus"), stackingPenalties=True)
    fit.ship.boostItemAttr("cpuOutput", src.getModifiedItemAttr("drawback"))
