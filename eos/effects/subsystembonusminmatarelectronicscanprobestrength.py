# subSystemBonusMinmatarElectronicScanProbeStrength
#
# Used by:
# Subsystem: Loki Electronics - Emergent Locus Analyzer
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength",
                                    module.getModifiedItemAttr("subsystemBonusMinmatarElectronic"),
                                    skill="Minmatar Electronic Systems")
