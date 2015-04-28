# shipBonusLargeEnergyTurretMaxRangeAB
#
# Used by:
# Ship: Paladin
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAB") * level)
