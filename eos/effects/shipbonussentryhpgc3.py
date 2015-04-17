# shipBonusSentryHPGC3
#
# Used by:
# Ship: Ishtar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "hp", ship.getModifiedItemAttr("shipBonusGC3") * level)
