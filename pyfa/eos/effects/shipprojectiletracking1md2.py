# shipProjectileTracking1MD2
#
# Used by:
# Variations of ship: Thrasher (3 of 3)
# Ship: Thrasher Thukker Tribe Edition
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusMD2") * level)
