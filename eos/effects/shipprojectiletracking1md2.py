# shipProjectileTracking1MD2
#
# Used by:
# Variations of ship: Thrasher (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusMD2") * level)
