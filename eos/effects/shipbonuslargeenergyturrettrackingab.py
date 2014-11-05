# shipBonusLargeEnergyTurretTrackingAB
#
# Used by:
# Ships named like: Apocalypse (5 of 6)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusAB") * level)
