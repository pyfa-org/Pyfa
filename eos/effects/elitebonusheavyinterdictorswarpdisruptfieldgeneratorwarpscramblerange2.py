# Used by:
# Ships from group: Heavy Interdiction Cruiser (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Interdiction Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Disrupt Field Generator",
                                  "warpScrambleRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors2") * level)