# Used by:
# Variations of module: Information Warfare Link - Electronic Superiority I (2 of 2)
gangBonus = "commandBonusECM"
gangBoost = "ewarStrECM"
type = "active", "gang"
def handler(fit, module, context):
    if "gang" not in context: return
    for scanType in ("Magnetometric", "Radar", "Ladar", "Gravimetric"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scan%sStrengthBonus" % scanType,
                                      module.getModifiedItemAttr("commandBonusECM"),
                                      stackingPenalties = True)
