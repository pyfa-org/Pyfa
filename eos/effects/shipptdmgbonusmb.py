# Used by:
# Ship: Machariel
# Ship: Panther
# Ship: Tempest
# Ship: Tempest Fleet Issue
# Ship: Tempest Tribal Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusMB") * level)
