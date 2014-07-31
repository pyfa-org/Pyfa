# Used by:
# Ship: Onyx
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Interdiction Cruisers").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1") * level)
