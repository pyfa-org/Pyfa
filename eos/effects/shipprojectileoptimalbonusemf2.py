# shipProjectileOptimalBonuseMF2
#
# Used by:
# Ship: Cheetah
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
