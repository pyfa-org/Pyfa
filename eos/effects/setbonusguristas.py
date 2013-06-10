# Used by:
# Implants named like: Crystal (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "shieldBoostMultiplier" in implant.itemModifiedAttributes and \
                                   "implantSetGuristas" in implant.itemModifiedAttributes,
                                   "shieldBoostMultiplier", implant.getModifiedItemAttr("implantSetGuristas"))