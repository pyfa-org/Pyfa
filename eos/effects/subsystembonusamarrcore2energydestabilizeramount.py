type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "energyNeutralizerAmount",
                                  src.getModifiedItemAttr("subsystemBonusAmarrCore2"), skill="Amarr Core Systems")
