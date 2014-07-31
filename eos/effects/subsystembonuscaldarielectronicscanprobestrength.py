# Used by:
# Subsystem: Tengu Electronics - Emergent Locus Analyzer
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Electronic Systems").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", module.getModifiedItemAttr("subsystemBonusCaldariElectronic") * level)
