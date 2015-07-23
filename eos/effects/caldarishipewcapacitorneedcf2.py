# caldariShipEwCapacitorNeedCF2
#
# Used by:
# Variations of ship: Griffin (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
