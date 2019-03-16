# battlecruiserDroneSpeed
#
# Used by:
# Ship: Myrmidon
# Ship: Prophecy
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxVelocity", ship.getModifiedItemAttr("roleBonusCBC"))
