# eliteBonusHeavyInterdictorsWarpDisruptFieldGeneratorWarpScrambleRange2
#
# Used by:
# Ships from group: Heavy Interdiction Cruiser (5 of 5)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Disrupt Field Generator",
                                  "warpScrambleRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors2"),
                                  skill="Heavy Interdiction Cruisers")
