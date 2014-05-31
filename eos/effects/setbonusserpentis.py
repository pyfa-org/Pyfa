# Used by:
# Implants named like: Low grade Snake (12 of 12)
# Implants named like: Snake (18 of 18)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "velocityBonus", implant.getModifiedItemAttr("implantSetSerpentis"))
