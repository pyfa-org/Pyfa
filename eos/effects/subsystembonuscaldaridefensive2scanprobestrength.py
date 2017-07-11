# subSystemBonusCaldariDefensive2ScanProbeStrength
#
# Used by:
# Subsystem: Tengu Defensive - Covert Reconfiguration
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseSensorStrength", src.getModifiedItemAttr("subsystemBonusCaldariDefensive2"),
                                    skill="Caldari Defensive Systems")
