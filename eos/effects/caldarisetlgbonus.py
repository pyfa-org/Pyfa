# Used by:
# Implants named like: Low grade Talon (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, item, context):
    fit.implants.filteredItemMultiply(lambda implant: "scanGravimetricStrengthModifier" in implant.itemModifiedAttributes,
                                   "scanGravimetricStrengthModifier", item.getModifiedItemAttr("implantSetLGCaldariNavy"))
