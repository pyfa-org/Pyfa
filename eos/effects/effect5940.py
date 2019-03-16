# eliteBonusInterdictorsSHTRoF1
#
# Used by:
# Ship: Eris
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("eliteBonusInterdictors1"), skill="Interdictors")
