# eliteBonusGunshipProjectileDamage1
#
# Used by:
# Ship: Wolf
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusGunship1"),
                                  skill="Assault Frigates")
