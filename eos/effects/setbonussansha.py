# setBonusSansha
#
# Used by:
# Implants named like: grade Slave (18 of 18)
# Implant: High-grade Halo Omega
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    print "applying set bonus to implants on ", fit, fit.appliedImplants, " from: ", implant, implant.item.name
    fit.appliedImplants.filteredItemMultiply(lambda target: target.item.requiresSkill("Cybernetics"),
                                      "armorHpBonus", implant.getModifiedItemAttr("implantSetSansha") or 1)
