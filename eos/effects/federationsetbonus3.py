# Used by:
# Implant: Spur Alpha
# Implant: Spur Beta
# Implant: Spur Delta
# Implant: Spur Epsilon
# Implant: Spur Gamma
# Implant: Spur Omega
type = "passive"
runTime = "early"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanMagnetometricStrengthPercent", implant.getModifiedItemAttr("implantSetFederationNavy"))
