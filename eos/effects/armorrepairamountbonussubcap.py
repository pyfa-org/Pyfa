# armorRepairAmountBonusSubcap
#
# Used by:
# Implants named like: grade Asklepian (15 of 18)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", src.getModifiedItemAttr("armorRepairBonus"))
