# Used by:
# Implants named like: Genolution Core Augmentation CA (2 of 2)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "cpuOutputBonus2" in implant.itemModifiedAttributes and \
                                      "implantSetChristmas" in implant.itemModifiedAttributes,
                                      "cpuOutputBonus2", implant.getModifiedItemAttr("implantSetChristmas"))
