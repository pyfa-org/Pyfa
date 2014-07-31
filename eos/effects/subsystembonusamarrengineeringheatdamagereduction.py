# Used by:
# Subsystem: Legion Engineering - Supplemental Coolant Injector
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Amarr Engineering Systems").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusAmarrEngineering") * level)
