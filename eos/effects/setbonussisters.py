# Used by:
# Implants named like: Low grade Virtue (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "scanStrengthBonus" in implant.itemModifiedAttributes and \
                                      "implantSetSisters" in implant.itemModifiedAttributes,
                                      "scanStrengthBonus", implant.getModifiedItemAttr("implantSetSisters"))