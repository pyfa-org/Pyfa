# shipBonusLargeEnergyWeaponDamageAB2
#
# Used by:
# Ships named like: Abaddon (3 of 3)
# Ship: 地狱天使级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusAB2") * level)
