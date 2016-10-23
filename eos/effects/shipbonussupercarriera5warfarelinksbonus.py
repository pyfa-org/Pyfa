# shipBonusSupercarrierA5WarfareLinksBonus
#
# Used by:
# Ship: Aeon
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusSupercarrierA5"), skill="Amarr Carrier")
