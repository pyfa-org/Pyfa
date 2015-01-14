# shipPTDmgBonusMB
#
# Used by:
# Ships named like: Tempest (6 of 6)
# Ship: Machariel
# Ship: Panther
# Ship: 马克瑞级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMB") * level)
