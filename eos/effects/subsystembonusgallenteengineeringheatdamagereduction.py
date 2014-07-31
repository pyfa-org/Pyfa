# Used by:
# Subsystem: Proteus Engineering - Supplemental Coolant Injector
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Engineering Systems").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  module.getModifiedItemAttr("subsystemBonusGallenteEngineering") * level)
