# subSystemBonusAmarrElectronic2TractorBeamVelocity
#
# Used by:
# Subsystem: Legion Electronics - Emergent Locus Analyzer
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", module.getModifiedItemAttr("subsystemBonusAmarrElectronic2"),
                                  skill="Amarr Electronic Systems")
