# setBonusThukker
#
# Used by:
# Implants named like: grade Nomad (12 of 12)
runTime = "early"
type = "passive"


def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                             "agilityBonus", implant.getModifiedItemAttr("implantSetThukker"))
