# subSystemBonusGallenteDefensive3TractorBeamBonus
#
# Used by:
# Subsystem: Proteus Defensive - Covert Reconfiguration
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam", "maxRange",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive3"), skill="Gallente Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam", "maxTractorVelocity",
                                  src.getModifiedItemAttr("subsystemBonusGallenteDefensive3"), skill="Gallente Defensive Systems")
