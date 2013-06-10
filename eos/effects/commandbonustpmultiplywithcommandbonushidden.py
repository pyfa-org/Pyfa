# Used by:
# Variations of module: Information Warfare Link - Electronic Superiority I (2 of 2)
gangBonus = "commandBonusTP"
gangBoost = "ewarStrTP"
type = "active", "gang"
def handler(fit, module, context):
    if "gang" not in context: return
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", module.getModifiedItemAttr("commandBonusTP"),
                                  stackingPenalties = True)
