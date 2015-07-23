# eliteBonusHeavyInterdictorLightMissileVelocityBonus
#
# Used by:
# Ship: Onyx
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"), skill="Heavy Interdiction Cruisers")
