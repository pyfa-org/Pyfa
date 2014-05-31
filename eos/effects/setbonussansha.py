# Used by:
# Implants named like: Low grade Slave (12 of 12)
# Implants named like: Slave (18 of 18)
# Implant: Halo Omega
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "armorHpBonus", implant.getModifiedItemAttr("implantSetSansha") or 1)
