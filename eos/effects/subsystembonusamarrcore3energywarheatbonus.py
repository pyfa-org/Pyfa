type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Energy Nosferatu", "Energy Neutralizer"), "overloadSelfDurationBonus",
                                  src.getModifiedItemAttr("subsystemBonusAmarrCore3"), skill="Amarr Core Systems")
