# shipBonusLargeEnergyTurretMaxRangeAB2
#
# Used by:
# Ship: Apocalypse
# Ship: Apocalypse Navy Issue
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")
