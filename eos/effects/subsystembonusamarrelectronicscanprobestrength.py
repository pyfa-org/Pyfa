# subSystemBonusAmarrElectronicScanProbeStrength
#
# Used by:
# Subsystem: Legion Electronics - Emergent Locus Analyzer
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", module.getModifiedItemAttr("subsystemBonusAmarrElectronic"), skill="Amarr Electronic Systems")
