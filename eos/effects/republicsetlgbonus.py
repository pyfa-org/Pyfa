# republicsetLGbonus
#
# Used by:
# Implants named like: Low grade Jackal (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanLadarStrengthModifier", implant.getModifiedItemAttr("implantSetLGRepublicFleet"))
