# Used by:
# Implants named like: Low grade Harvest (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "maxRangeBonus" in implant.itemModifiedAttributes and \
                                      "implantSetORE" in implant.itemModifiedAttributes,
                                      "maxRangeBonus", implant.getModifiedItemAttr("implantSetORE"))