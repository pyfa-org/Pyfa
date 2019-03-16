# eliteBonusHeavyGunshipProjectileTracking2
#
# Used by:
# Ship: Muninn
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                  skill="Heavy Assault Cruisers")
