# Used by:
# Implants named like: Grail (6 of 12)
type = "passive"
runTime = "early"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "scanRadarStrengthPercent" in implant.itemModifiedAttributes and\
                                      "implantSetImperialNavy" in implant.itemModifiedAttributes,
                                      "scanRadarStrengthPercent", implant.getModifiedItemAttr("implantSetImperialNavy"))
