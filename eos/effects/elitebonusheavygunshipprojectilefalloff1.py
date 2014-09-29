# eliteBonusHeavyGunshipProjectileFallOff1
#
# Used by:
# Ship: Vagabond
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusHeavyGunship1") * level)
