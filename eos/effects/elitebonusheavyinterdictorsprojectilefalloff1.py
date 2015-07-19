# eliteBonusHeavyInterdictorsProjectileFalloff1
#
# Used by:
# Ship: Broadsword
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"), skill="Heavy Interdiction Cruisers")
