# eliteBonusHeavyInterdictorHeavyAssaultMissileVelocityBonus
#
# Used by:
# Ship: Onyx
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                    skill="Heavy Interdiction Cruisers")
