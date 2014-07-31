# Used by:
# Subsystem: Tengu Engineering - Supplemental Coolant Injector
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Engineering Systems").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusCaldariEngineering") * level)
