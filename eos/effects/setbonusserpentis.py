# setBonusSerpentis
#
# Used by:
# Implants named like: grade Snake (18 of 18)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "velocityBonus", implant.getModifiedItemAttr("implantSetSerpentis"))
