# Used by:
# Implants named like: Crystal (18 of 18)
# Implants named like: Low grade Crystal (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda mod: mod.item.group.name == "Cyberimplant",
                                      "shieldBoostMultiplier", implant.getModifiedItemAttr("implantSetGuristas"))
