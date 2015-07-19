# subsystemBonusAmarrElectronicEnergyVampireAmount
#
# Used by:
# Subsystem: Legion Electronics - Energy Parasitic Complex
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferAmount", module.getModifiedItemAttr("subsystemBonusAmarrElectronic"), skill="Amarr Electronic Systems")
