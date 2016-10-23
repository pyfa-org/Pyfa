# shipBonusForceAuxiliaryA4WarfareLinksBonus
#
# Used by:
# Ship: Apostle
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryA4"), skill="Amarr Carrier")
