# eliteBonusHeavyGunshipProjectileTracking2
#
# Used by:
# Ship: Muninn
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2") * level)
