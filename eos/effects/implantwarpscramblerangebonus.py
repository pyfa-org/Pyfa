# implantWarpScrambleRangeBonus
#
# Used by:
# Implants named like: Inquest 'Hedone' Entanglement Optimizer WS (3 of 3)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler", "maxRange",
                                  src.getModifiedItemAttr("warpScrambleRangeBonus"), stackingPenalties=False)
