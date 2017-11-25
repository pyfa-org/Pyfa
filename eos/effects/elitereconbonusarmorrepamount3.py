# eliteReconBonusArmorRepAmount3
#
# Used by:
# Ship: Victor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"), "armorDamageAmount",
                                  src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")
