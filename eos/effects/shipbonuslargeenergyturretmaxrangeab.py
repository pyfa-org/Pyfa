# shipBonusLargeEnergyTurretMaxRangeAB
#
# Used by:
# Ships named like: Paladin (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAB") * level)
