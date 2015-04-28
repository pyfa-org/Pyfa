# shipBonusScanProbeStrengthCF
#
# Used by:
# Ship: Heron
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", ship.getModifiedItemAttr("shipBonusCF2") * level)