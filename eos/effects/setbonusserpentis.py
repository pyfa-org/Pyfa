# Used by:
# Implants named like: Snake (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "velocityBonus" in implant.itemModifiedAttributes and \
                                      "implantSetSerpentis" in implant.itemModifiedAttributes,
                                      "velocityBonus", implant.getModifiedItemAttr("implantSetSerpentis"))