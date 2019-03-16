# shipBonusScanProbeStrengthMF
#
# Used by:
# Ship: Probe
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", ship.getModifiedItemAttr("shipBonusMF2"),
                                    skill="Minmatar Frigate")
