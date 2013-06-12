# Used by:
# Variations of module: Scan Pinpointing Array I (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseMaxScanDeviation", module.getModifiedItemAttr("maxScanDeviationModifierModule"),
                                    stackingPenalties=True)
