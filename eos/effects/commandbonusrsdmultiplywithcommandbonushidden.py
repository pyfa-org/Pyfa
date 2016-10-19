# commandBonusRSDMultiplyWithCommandBonusHidden
#
# Used by:
# Variations of module: Information Warfare Link - Electronic Superiority I (2 of 2)
gangBonus = "commandBonusRSD"
gangBoost = "ewarStrRSD"
type = "active", "gang"


def handler(fit, module, context):
    if "gang" not in context: return
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Sensor Linking"),
                                  "maxTargetRangeBonus", module.getModifiedItemAttr("commandBonusRSD"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Sensor Linking"),
                                  "scanResolutionBonus", module.getModifiedItemAttr("commandBonusRSD"),
                                  stackingPenalties=True)
