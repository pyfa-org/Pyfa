# setBonusChristmasShieldCapacityBonus
#
# Used by:
# Implants named like: Genolution Core Augmentation CA (4 of 4)
runTime = "early"
type = "passive"


def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.group.name == "Special Edition Implant",
                                             "shieldCapacityBonus", implant.getModifiedItemAttr("implantSetChristmas"))
