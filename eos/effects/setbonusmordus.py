# Used by:
# Implants named like: Low grade Centurion (6 of 6)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "rangeSkillBonus" in implant.itemModifiedAttributes and \
                                   "implantSetMordus" in implant.itemModifiedAttributes,
                                   "rangeSkillBonus", implant.getModifiedItemAttr("implantSetMordus"))