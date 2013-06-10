# Used by:
# Implants named like: Genolution Core Augmentation CA (2 of 2)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "capacitorCapacityBonus" in implant.itemModifiedAttributes and \
                                      "implantSetChristmas" in implant.itemModifiedAttributes,
                                      "capacitorCapacityBonus", implant.getModifiedItemAttr("implantSetChristmas"))
