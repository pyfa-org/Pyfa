# Used by:
# Implants named like: Low grade Spur (6 of 6)
type = "passive"
runTime = "early"
def handler(fit, item, context):
    fit.implants.filteredItemMultiply(lambda implant: "scanMagnetometricStrengthModifier" in implant.itemModifiedAttributes,
                                      "scanMagnetometricStrengthModifier", item.getModifiedItemAttr("implantSetLGFederationNavy"))
