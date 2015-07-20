# shipBonusScanProbeStrengthGF
#
# Used by:
# Ship: Imicus
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
