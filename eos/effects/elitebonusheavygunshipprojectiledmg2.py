# eliteBonusHeavyGunshipProjectileDmg2
#
# Used by:
# Ship: Vagabond
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"), skill="Heavy Assault Cruisers")
