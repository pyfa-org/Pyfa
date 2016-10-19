# eliteBonusHeavyInterdictorsMETOptimal
#
# Used by:
# Ship: Devoter
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                  skill="Heavy Interdiction Cruisers")
