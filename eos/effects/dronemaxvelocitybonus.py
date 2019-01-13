# droneMaxVelocityBonus
#
# Used by:
# Modules named like: Drone Speed Augmentor (6 of 8)
# Implant: Overmind 'Goliath' Drone Tuner T25-10S
# Implant: Overmind 'Hawkmoth' Drone Tuner S10-25T
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxVelocity", container.getModifiedItemAttr("droneMaxVelocityBonus") * level, stackingPenalties=True)
