# Used by:
# Implants named like: Spur (6 of 12)
type = "passive"
runTime = "early"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "implantSetFederationNavy" in implant.itemModifiedAttributes and\
                                   "scanMagnetometricStrengthPercent" in implant.itemModifiedAttributes,
                                   "scanMagnetometricStrengthPercent", implant.getModifiedItemAttr("implantSetFederationNavy"))