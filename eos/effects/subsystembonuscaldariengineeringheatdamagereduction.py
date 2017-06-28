# subsystemBonusCaldariEngineeringHeatDamageReduction
#
# Used by:
# Subsystem: Tengu Core - Obfuscation Manifold
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusCaldariCore"),
                                  skill="Caldari Core Systems")
