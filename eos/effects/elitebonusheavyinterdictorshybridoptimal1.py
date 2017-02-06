# eliteBonusHeavyInterdictorsHybridOptimal1
#
# Used by:
# Ship: Phobos
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1"),
                                  skill="Heavy Interdiction Cruisers")
