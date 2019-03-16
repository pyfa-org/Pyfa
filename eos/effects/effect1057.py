# eliteBonusHeavyGunshipProjectileOptimal1
#
# Used by:
# Ship: Muninn
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                  skill="Heavy Assault Cruisers")
