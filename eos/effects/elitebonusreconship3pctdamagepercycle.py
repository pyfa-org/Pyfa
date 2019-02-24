# eliteBonusReconShip3PCTdamagePerCycle
#
# Used by:
# Ship: Tiamat
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"), "damageMultiplierBonusPerCycle",
                                     src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")
