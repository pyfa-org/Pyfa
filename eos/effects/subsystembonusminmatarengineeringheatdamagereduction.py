# subsystemBonusMinmatarEngineeringHeatDamageReduction
#
# Used by:
# Subsystem: Loki Core - Immobility Drivers
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusMinmatarCore"),
                                  skill="Minmatar Core Systems")
