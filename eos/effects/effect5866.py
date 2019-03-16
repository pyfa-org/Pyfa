# shipBonusWarpScrambleMaxRangeGB
#
# Used by:
# Ship: Barghest
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")
