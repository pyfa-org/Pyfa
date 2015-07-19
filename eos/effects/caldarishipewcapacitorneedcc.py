# caldariShipEwCapacitorNeedCC
#
# Used by:
# Ship: Chameleon
# Ship: Falcon
# Ship: Rook
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusCC", skill="Caldari Cruiser")
