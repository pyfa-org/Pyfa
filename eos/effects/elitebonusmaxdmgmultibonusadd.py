# eliteBonusMaxDmgMultiBonusAdd
#
# Used by:
# Ship: Hydra
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"), "damageMultiplierBonusMax",
                                     src.getModifiedItemAttr("eliteBonusCovertOps3"), skill="Covert Ops")
