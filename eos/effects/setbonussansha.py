# Used by:
# Implants named like: Slave (12 of 12)
# Implant: Halo Omega
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda implant: "armorHpBonus" in implant.itemModifiedAttributes and \
                                      "implantSetSansha" in implant.itemModifiedAttributes,
                                      "armorHpBonus", implant.getModifiedItemAttr("implantSetSansha"))