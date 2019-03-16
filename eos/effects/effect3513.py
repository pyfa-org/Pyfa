# setBonusMordus
#
# Used by:
# Implants named like: grade Centurion (12 of 12)
runTime = "early"
type = "passive"


def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                             "rangeSkillBonus", implant.getModifiedItemAttr("implantSetMordus"))
