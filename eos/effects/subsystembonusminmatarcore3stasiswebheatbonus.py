type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "overloadRangeBonus", src.getModifiedItemAttr("subsystemBonusMinmatarCore3"),
                                  skill="Minmatar Core Systems")
