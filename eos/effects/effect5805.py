# shipBonusSentryDroneHPPirateFaction
#
# Used by:
# Ship: Rattlesnake
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "hp", ship.getModifiedItemAttr("shipBonusRole7"))
