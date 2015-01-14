# shipProjectileRofPirateBattleship
#
# Used by:
# Ship: Machariel
# Ship: 马克瑞级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusPirateFaction"))
