# Used by:
# Implants named like: High grade Spur (6 of 6)
type = "passive"
runTime = "early"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanMagnetometricStrengthPercent", implant.getModifiedItemAttr("implantSetFederationNavy"))
