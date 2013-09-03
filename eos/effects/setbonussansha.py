# Used by:
# Implants named like: Slave (12 of 12)
# Implant: Halo Omega
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "armorHpBonus", implant.getModifiedItemAttr("implantSetSansha") or 1)
