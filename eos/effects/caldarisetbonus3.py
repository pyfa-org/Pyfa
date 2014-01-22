# Used by:
# Implant: Talon Alpha
# Implant: Talon Beta
# Implant: Talon Delta
# Implant: Talon Epsilon
# Implant: Talon Gamma
# Implant: Talon Omega
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanGravimetricStrengthPercent", implant.getModifiedItemAttr("implantSetCaldariNavy"))
