# subSystemBonusMinmatarElectronic2TractorBeamVelocity
#
# Used by:
# Subsystem: Loki Electronics - Emergent Locus Analyzer
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic2"), skill="Minmatar Electronic Systems")
