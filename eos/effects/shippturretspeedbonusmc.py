# Used by:
# Ships named like: Stabber (4 of 4)
# Variations of ship: Rupture (3 of 3)
# Variations of ship: Stabber (3 of 3)
# Ship: Huginn
# Ship: Rapier
# Ship: Scythe Fleet Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMC") * level)
