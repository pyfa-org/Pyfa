# Used by:
# Variations of module: Skirmish Warfare Link - Rapid Deployment I (2 of 2)
type = "gang", "active"
gangBoost = "speedFactor"
def handler(fit, module, context):
    if "gang" not in context: return
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                  "speedFactor", module.getModifiedItemAttr("commandBonus"),
                                  stackingPenalties = True)
