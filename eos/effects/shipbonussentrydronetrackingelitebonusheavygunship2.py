# Used by:
# Ship: Ishtar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "trackingSpeed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2") * level)
