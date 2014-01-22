# Used by:
# Implant: Genolution Core Augmentation CA-1
# Implant: Genolution Core Augmentation CA-2
# Implant: Genolution Core Augmentation CA-3
# Implant: Genolution Core Augmentation CA-4
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "cpuOutputBonus2", implant.getModifiedItemAttr("implantSetChristmas"))
