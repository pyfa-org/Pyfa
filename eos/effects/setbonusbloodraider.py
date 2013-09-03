# Used by:
# Implants named like: Talisman (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "durationBonus", implant.getModifiedItemAttr("implantSetBloodraider"))
