# Used by:
# Implants named like: Low grade Nomad (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "agilityBonus" in implant.itemModifiedAttributes and \
                                      "implantSetThukker" in implant.itemModifiedAttributes,
                                      "agilityBonus", implant.getModifiedItemAttr("implantSetThukker"))