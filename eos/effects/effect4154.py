# subsystemBonusGallenteEngineeringHeatDamageReduction
#
# Used by:
# Subsystem: Proteus Core - Friction Extension Processor
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusGallenteCore"),
                                  skill="Gallente Core Systems")
