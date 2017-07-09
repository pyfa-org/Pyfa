# subsystemBonusAmarrEngineeringHeatDamageReduction
#
# Used by:
# Subsystem: Legion Core - Energy Parasitic Complex
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusAmarrCore"),
                                  skill="Amarr Core Systems")
