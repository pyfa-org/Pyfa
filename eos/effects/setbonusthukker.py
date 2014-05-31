# Used by:
# Implants named like: Low grade Nomad (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "agilityBonus", implant.getModifiedItemAttr("implantSetThukker"))
