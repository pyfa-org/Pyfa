# imperialsetbonus3
#
# Used by:
# Implants named like: High grade Grail (6 of 6)
type = "passive"
runTime = "early"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "scanRadarStrengthPercent", implant.getModifiedItemAttr("implantSetImperialNavy"))
