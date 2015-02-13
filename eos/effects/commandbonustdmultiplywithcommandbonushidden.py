# commandBonusTDMultiplyWithCommandBonusHidden
#
# Used by:
# Variations of module: Information Warfare Link - Electronic Superiority I (2 of 2)
gangBonus = "commandBonusTD"
gangBoost = "ewarStrTD"
type = "active", "gang"
def handler(fit, module, context):
    if "gang" not in context: return
    for bonus in ("maxRangeBonus", "falloffBonus", "trackingSpeedBonus"):
        fit.modules.filteredItemBoost(lambda mod: lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                      bonus, module.getModifiedItemAttr("commandBonusTD"))
