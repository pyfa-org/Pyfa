# subSystemBonusCaldariElectronic2TractorBeamRange
#
# Used by:
# Subsystem: Tengu Electronics - Emergent Locus Analyzer
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusCaldariElectronic2"), skill="Caldari Electronic Systems")
