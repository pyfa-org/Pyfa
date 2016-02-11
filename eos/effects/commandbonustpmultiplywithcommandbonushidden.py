# commandBonusTPMultiplyWithCommandBonusHidden
#
# Used by:
# Variations of module: Information Warfare Link - Electronic Superiority I (2 of 2)
gangBonus = "commandBonusTP"
gangBoost = "ewarStrTP"
type = "active", "gang"
runTime = "late"

def handler(fit, module, context):
    if "gang" not in context: return
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Target Painting"),
                                  "signatureRadiusBonus", module.getModifiedItemAttr("commandBonusTP"),
                                  stackingPenalties = True)
