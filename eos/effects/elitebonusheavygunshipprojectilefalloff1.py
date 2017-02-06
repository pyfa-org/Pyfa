# eliteBonusHeavyGunshipProjectileFallOff1
#
# Used by:
# Ship: Vagabond
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"),
                                  skill="Heavy Assault Cruisers")
