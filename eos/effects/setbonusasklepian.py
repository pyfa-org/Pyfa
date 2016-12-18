# setBonusAsklepian
#
# Used by:
# Implants named like: Asklepian Omega (3 of 3)
# Implants named like: Grade Asklepian (16 of 16)
runTime = "early"
type = "passive"


def handler(fit, src, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Cybernetics"),
                                             "armorRepairBonus", src.getModifiedItemAttr("implantSetSerpentis2"))
