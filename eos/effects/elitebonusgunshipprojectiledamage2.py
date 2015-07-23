# eliteBonusGunshipProjectileDamage2
#
# Used by:
# Ship: Jaguar
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")