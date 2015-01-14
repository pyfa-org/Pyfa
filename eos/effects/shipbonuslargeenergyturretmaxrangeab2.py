# shipBonusLargeEnergyTurretMaxRangeAB2
#
# Used by:
# Ships named like: Apocalypse (5 of 6)
# Ship: 灾难级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAB2") * level)
