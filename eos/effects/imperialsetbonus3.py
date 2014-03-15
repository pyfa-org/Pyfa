# Used by:
# Implants named like: Grail (6 of 12)
type = "passive"
runTime = "early"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanRadarStrengthPercent", implant.getModifiedItemAttr("implantSetImperialNavy"))
