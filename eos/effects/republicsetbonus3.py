# Used by:
# Implants named like: Jackal (6 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "implantSetRepublicFleet" in implant.itemModifiedAttributes and\
                                   "scanLadarStrengthPercent" in implant.itemModifiedAttributes,
                                   "scanLadarStrengthPercent", implant.getModifiedItemAttr("implantSetRepublicFleet"))