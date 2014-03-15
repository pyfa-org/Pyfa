# Used by:
# Variations of ship: Tempest (3 of 4)
# Ship: Machariel
# Ship: Panther
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMB") * level)
