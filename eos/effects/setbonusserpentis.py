# Used by:
# Implants named like: Snake (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "velocityBonus", implant.getModifiedItemAttr("implantSetSerpentis"))
