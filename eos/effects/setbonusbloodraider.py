# Used by:
# Implants named like: Talisman (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "durationBonus" in implant.itemModifiedAttributes and \
                                      "implantSetBloodraider" in implant.itemModifiedAttributes,
                                      "durationBonus", implant.getModifiedItemAttr("implantSetBloodraider"))
