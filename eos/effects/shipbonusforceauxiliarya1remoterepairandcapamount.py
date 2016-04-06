type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Capacitor Emission Systems"), "powerTransferAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"), "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"), skill="Amarr Carrier")
