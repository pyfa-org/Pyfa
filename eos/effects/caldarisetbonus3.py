# Used by:
# Implants named like: Talon (6 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "implantSetCaldariNavy" in implant.itemModifiedAttributes and\
                                      "scanGravimetricStrengthPercent" in implant.itemModifiedAttributes,
                                      "scanGravimetricStrengthPercent", implant.getModifiedItemAttr("implantSetCaldariNavy"))
