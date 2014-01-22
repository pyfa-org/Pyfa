# Used by:
# Implants named like: grade Jackal (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanLadarStrengthModifier", implant.getModifiedItemAttr("implantSetLGRepublicFleet"))
