# shipGCHYieldBonusOREfrig2
#
# Used by:
# Variations of ship: Venture (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Gas Cloud Harvester",
                                  "duration", module.getModifiedItemAttr("shipBonusOREfrig2"), skill="Mining Frigate")
