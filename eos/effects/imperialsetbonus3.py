# Used by:
# Implant: Grail Alpha
# Implant: Grail Beta
# Implant: Grail Delta
# Implant: Grail Epsilon
# Implant: Grail Gamma
# Implant: Grail Omega
type = "passive"
runTime = "early"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanRadarStrengthPercent", implant.getModifiedItemAttr("implantSetImperialNavy"))
