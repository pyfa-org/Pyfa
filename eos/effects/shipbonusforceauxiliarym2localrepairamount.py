# shipBonusForceAuxiliaryM2LocalRepairAmount
#
# Used by:
# Ship: Dagon
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryM2"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"),
                                  "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryM2"), skill="Minmatar Carrier")
