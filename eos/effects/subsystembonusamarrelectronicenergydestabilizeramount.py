# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyNeutralizerAmount",
                                  module.getModifiedItemAttr("subsystemBonusAmarrElectronic"),
                                  skill="Amarr Electronic Systems")
