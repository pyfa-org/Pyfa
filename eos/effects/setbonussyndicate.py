# Used by:
# Implants named like: Low grade Edge (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "boosterAttributeModifier" in implant.itemModifiedAttributes and \
                                      "implantSetSyndicate" in implant.itemModifiedAttributes,
                                      "boosterAttributeModifier", implant.getModifiedItemAttr("implantSetSyndicate"))