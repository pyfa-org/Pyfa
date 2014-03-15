# Used by:
# Ships named like: Maelstrom (2 of 2)
# Variations of ship: Tempest (4 of 4)
# Ship: Panther
# Ship: Typhoon Fleet Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMB2") * level)
