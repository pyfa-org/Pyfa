# subSystemBonusMinmatarDefensive2ScanProbeStrength
#
# Used by:
# Subsystem: Loki Defensive - Covert Reconfiguration
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"), "baseSensorStrength",
                                    src.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")
