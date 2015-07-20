# shipBonusLargeEnergyTurretTrackingAB
#
# Used by:
# Ship: Apocalypse
# Ship: Apocalypse Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")
