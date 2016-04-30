# shipBonusForceAuxiliaryG2LocalRepairAmount
#
# Used by:
# Ship: Ninazu
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"), "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryG2"), skill="Gallente Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Repair Systems"), "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryG2"), skill="Gallente Carrier")
