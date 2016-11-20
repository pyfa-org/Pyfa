# subSystemBonusGallenteElectronic2TractorBeamVelocity
#
# Used by:
# Subsystem: Proteus Electronics - Emergent Locus Analyzer
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", module.getModifiedItemAttr("subsystemBonusGallenteElectronic2"),
                                  skill="Gallente Electronic Systems")
