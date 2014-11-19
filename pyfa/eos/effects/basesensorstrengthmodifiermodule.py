# baseSensorStrengthModifierModule
#
# Used by:
# Variations of module: Scan Rangefinding Array I (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseSensorStrength", module.getModifiedItemAttr("scanStrengthBonusModule"),
                                    stackingPenalties=True)
