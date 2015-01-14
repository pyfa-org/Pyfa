# shipBonusSentryDroneOptimalRangeEliteBonusHeavyGunship2
#
# Used by:
# Ship: Ishtar
# Ship: 伊什塔级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship2") * level)
