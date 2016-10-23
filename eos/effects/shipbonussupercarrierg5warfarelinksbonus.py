# shipBonusSupercarrierG5WarfareLinksBonus
#
# Used by:
# Ship: Nyx
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")
