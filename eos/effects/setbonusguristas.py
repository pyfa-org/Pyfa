# setBonusGuristas
#
# Used by:
# Implants named like: grade Crystal (18 of 18)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "shieldBoostMultiplier", implant.getModifiedItemAttr("implantSetGuristas"))
