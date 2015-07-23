# shipBonusWarpScramblerMaxRangeGF2
#
# Used by:
# Ship: Garmur
# Ship: Utu
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
