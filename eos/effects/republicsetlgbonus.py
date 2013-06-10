# Used by:
# Implants named like: Low grade Jackal (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, item, context):
    fit.implants.filteredItemMultiply(lambda implant: "scanLadarStrengthModifier" in implant.itemModifiedAttributes,
                                      "scanLadarStrengthModifier", item.getModifiedItemAttr("implantSetLGRepublicFleet"))
