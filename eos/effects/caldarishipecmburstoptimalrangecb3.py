# caldariShipECMBurstOptimalRangeCB3
#
# Used by:
# Ship: Scorpion
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM Burst",
                                  "ecmBurstRange", ship.getModifiedItemAttr("shipBonusCB3"), skill="Caldari Battleship")
