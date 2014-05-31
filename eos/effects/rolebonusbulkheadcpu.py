# Used by:
# Ships from group: Freighter (4 of 4)
# Ships from group: Jump Freighter (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Reinforced Bulkhead",
                                  "cpu", ship.getModifiedItemAttr("cpuNeedBonus"))
