# eliteBonusReconMaxDmgMultiMaxHPT
#
# Used by:
# Ship: Tiamat
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"), "damageMultiplierBonusMax",
                                     src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")
