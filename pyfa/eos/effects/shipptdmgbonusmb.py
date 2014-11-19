# shipPTDmgBonusMB
#
# Used by:
# Ships named like: Tempest (6 of 6)
# Ship: Machariel
# Ship: Panther
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMB") * level)
