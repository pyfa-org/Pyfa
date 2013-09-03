# Used by:
# Implants named like: Low grade Harvest (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "maxRangeBonus", implant.getModifiedItemAttr("implantSetORE"))
