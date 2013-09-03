# Used by:
# Implants named like: Crystal (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "shieldBoostMultiplier", implant.getModifiedItemAttr("implantSetGuristas"))
