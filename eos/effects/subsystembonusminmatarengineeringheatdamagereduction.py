# subsystemBonusMinmatarEngineeringHeatDamageReduction
#
# Used by:
# Subsystem: Loki Engineering - Supplemental Coolant Injector
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusMinmatarEngineering"),
                                  skill="Minmatar Engineering Systems")
