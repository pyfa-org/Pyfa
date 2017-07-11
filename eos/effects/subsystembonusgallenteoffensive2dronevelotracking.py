# subsystemBonusGallenteOffensive2DroneVeloTracking
#
# Used by:
# Subsystem: Proteus Offensive - Drone Synthesis Projector
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "maxVelocity", src.getModifiedItemAttr("subsystemBonusGallenteOffensive2"),
                                 skill="Gallente Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "trackingSpeed", src.getModifiedItemAttr("subsystemBonusGallenteOffensive2"),
                                 skill="Gallente Offensive Systems")
