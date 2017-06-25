# subSystemBonusAmarrDefensiveScanProbeStrength2
#
# Used by:
# Subsystem: Legion Defensive - Covert Reconfiguration
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                  "baseSensorStrength", module.getModifiedItemAttr("subsystemBonusAmarrDefensive2"),
                                  skill="Amarr Defensive Systems")
