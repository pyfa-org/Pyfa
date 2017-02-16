# setBonusAsklepian
#
# Used by:
# Implants named like: grade Asklepian (18 of 18)
runTime = "early"
type = "passive"


def handler(fit, src, context):
    fit.appliedImplants.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Cybernetics"),
                                             "armorRepairBonus", src.getModifiedItemAttr("implantSetSerpentis2"))
