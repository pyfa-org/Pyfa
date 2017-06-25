# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferAmount", module.getModifiedItemAttr("subsystemBonusAmarrElectronic"),
                                  skill="Amarr Electronic Systems")
