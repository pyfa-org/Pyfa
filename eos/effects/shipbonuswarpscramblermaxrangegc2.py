# shipBonusWarpScramblerMaxRangeGC2
#
# Used by:
# Ship: Adrestia
# Ship: Orthrus
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
