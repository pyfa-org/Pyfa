# eliteBonusHeavyInterdictorHeavyMissileVelocityBonus1
#
# Used by:
# Ship: Onyx
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"), skill="Heavy Interdiction Cruisers")
