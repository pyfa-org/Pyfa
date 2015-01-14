# shipPTurretFalloffBonusGB
#
# Used by:
# Ship: Machariel
# Ship: 马克瑞级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusGB") * level)