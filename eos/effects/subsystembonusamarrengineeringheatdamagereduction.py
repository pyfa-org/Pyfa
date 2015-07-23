# subsystemBonusAmarrEngineeringHeatDamageReduction
#
# Used by:
# Subsystem: Legion Engineering - Supplemental Coolant Injector
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusAmarrEngineering"), skill="Amarr Engineering Systems")
