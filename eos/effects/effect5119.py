# shipBonusScanProbeStrength2AF
#
# Used by:
# Ship: Magnate
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", ship.getModifiedItemAttr("shipBonus2AF"),
                                    skill="Amarr Frigate")
