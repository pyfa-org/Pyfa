# Used by:
# Implants named like: Spur (6 of 12)
type = "passive"
runTime = "early"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanMagnetometricStrengthPercent", implant.getModifiedItemAttr("implantSetFederationNavy"))
