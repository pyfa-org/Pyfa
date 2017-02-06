# setBonusBloodraider
#
# Used by:
# Implants named like: grade Talisman (18 of 18)
runTime = "early"
type = "passive"


def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                             "durationBonus", implant.getModifiedItemAttr("implantSetBloodraider"))
