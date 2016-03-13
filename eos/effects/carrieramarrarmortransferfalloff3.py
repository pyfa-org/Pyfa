# carrierAmarrArmorTransferFalloff3
#
# Used by:
# Ship: Aeon
# Ship: Archon
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"), "falloffEffectiveness", src.getModifiedItemAttr("carrierAmarrBonus3"), skill="Amarr Carrier")
