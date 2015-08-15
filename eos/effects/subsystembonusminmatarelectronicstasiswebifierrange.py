# subsystemBonusMinmatarElectronicStasisWebifierRange
#
# Used by:
# Subsystem: Loki Electronics - Immobility Drivers
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic"), skill="Minmatar Electronic Systems")
