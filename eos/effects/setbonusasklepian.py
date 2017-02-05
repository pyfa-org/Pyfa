# setBonusAsklepian
#
# Used by:
# Implants named like: Grade Asklepian (16 of 16)
# Implants named like: grade Asklepian Omega (2 of 2)
runTime = "early"
type = "passive"


def handler(fit, src, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Cybernetics"),
                                             "armorRepairBonus", src.getModifiedItemAttr("implantSetSerpentis2"))
