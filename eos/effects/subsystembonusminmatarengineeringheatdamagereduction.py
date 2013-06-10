# Used by:
# Subsystem: Loki Engineering - Supplemental Coolant Injector
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Engineering Systems").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusMinmatarEngineering") * level)
