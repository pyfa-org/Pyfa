# Used by:
# Subsystem: Loki Electronics - Emergent Locus Analyzer
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Electronic Systems").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic") * level)
