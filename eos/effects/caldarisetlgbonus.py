# Used by:
# Implants named like: Low grade Talon (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanGravimetricStrengthModifier", implant.getModifiedItemAttr("implantSetLGCaldariNavy"))
