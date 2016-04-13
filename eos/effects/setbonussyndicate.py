# setBonusSyndicate
#
# Used by:
# Implants named like: grade Edge (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "boosterAttributeModifier", implant.getModifiedItemAttr("implantSetSyndicate"))
