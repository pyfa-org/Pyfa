# Used by:
# Variations of module: Information Warfare Link - Electronic Superiority I (2 of 2)
gangBonus = "commandBonusTD"
gangBoost = "ewarStrTD"
type = "active", "gang"
def handler(fit, module, context):
    for bonus in ("maxRangeBonus", "falloffBonus", "trackingSpeedBonus"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                      bonus, module.getModifiedItemAttr("commandBonusTD"),
                                      stackingPenalties = True)
