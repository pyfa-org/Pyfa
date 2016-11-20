# shipBonusSupercarrierG5WarfareLinksBonus
#
# Used by:
# Ship: Nyx
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Warfare Specialist"), "commandBonus",
                                  src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Warfare Specialist"), "commandBonus",
                                  src.getModifiedItemAttr("shipBonusSupercarrierG5"), skill="Gallente Carrier")
