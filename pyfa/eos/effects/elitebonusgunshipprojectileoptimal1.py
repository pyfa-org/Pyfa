# eliteBonusGunshipProjectileOptimal1
#
# Used by:
# Ship: Jaguar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Assault Frigates").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusGunship1") * level)