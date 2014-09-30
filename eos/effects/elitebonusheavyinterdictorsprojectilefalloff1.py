# eliteBonusHeavyInterdictorsProjectileFalloff1
#
# Used by:
# Ship: Broadsword
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Interdiction Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1") * level)
