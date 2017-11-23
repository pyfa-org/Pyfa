# shipBonusLargeEnergyTurretMaxRangeAB
#
# Used by:
# Ship: Marshal
# Ship: Paladin
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")
