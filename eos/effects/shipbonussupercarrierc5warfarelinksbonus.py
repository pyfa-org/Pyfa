# shipBonusSupercarrierC5WarfareLinksBonus
#
# Used by:
# Ship: Wyvern
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusSupercarrierC5"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusSupercarrierC5"), skill="Caldari Carrier")
