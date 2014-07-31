# Used by:
# Variations of module: Skirmish Warfare Link - Interdiction Maneuvers I (2 of 2)
type = "gang", "active"
gangBoost = "interdictionMaxRange"
def handler(fit, module, context):
    if "gang" not in context: return
    groups = ("Stasis Web","Warp Scrambler")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "maxRange", module.getModifiedItemAttr("commandBonus"),
                                  stackingPenalties = True)
