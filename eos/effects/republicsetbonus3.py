# Used by:
# Implants named like: Jackal (6 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanLadarStrengthPercent", implant.getModifiedItemAttr("implantSetRepublicFleet"))
