# Used by:
# Implants named like: Talon (6 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanGravimetricStrengthPercent", implant.getModifiedItemAttr("implantSetCaldariNavy"))
