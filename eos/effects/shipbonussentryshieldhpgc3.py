# shipBonusSentryShieldHPGC3
#
# Used by:
# Ship: Ishtar
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "shieldCapacity", ship.getModifiedItemAttr("shipBonusGC3"), skill="Gallente Cruiser")
