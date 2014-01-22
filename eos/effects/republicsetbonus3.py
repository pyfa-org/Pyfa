# Used by:
# Implant: Jackal Alpha
# Implant: Jackal Beta
# Implant: Jackal Delta
# Implant: Jackal Epsilon
# Implant: Jackal Gamma
# Implant: Jackal Omega
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanLadarStrengthPercent", implant.getModifiedItemAttr("implantSetRepublicFleet"))
