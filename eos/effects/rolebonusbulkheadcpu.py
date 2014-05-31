type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Reinforced Bulkhead",
                                  "cpu", ship.getModifiedItemAttr("cpuNeedBonus"))
