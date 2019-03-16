# subsystemBonusCaldariPropulsion2PropModHeatBenefit
#
# Used by:
# Subsystem: Tengu Propulsion - Fuel Catalyst
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner") or mod.item.requiresSkill("High Speed Maneuvering"),
                                  "overloadSpeedFactorBonus", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                                  skill="Caldari Propulsion Systems")
