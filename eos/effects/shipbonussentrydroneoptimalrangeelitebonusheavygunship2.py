# shipBonusSentryDroneOptimalRangeEliteBonusHeavyGunship2
#
# Used by:
# Ship: Ishtar
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"), skill="Heavy Assault Cruisers")
