# shipBonusCarrierA4WarfareLinksBonus
#
# Used by:
# Ship: Archon
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"), "commandBonus",
                                  src.getModifiedItemAttr("shipBonusCarrierA4"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Warfare Specialist"), "commandBonus",
                                  src.getModifiedItemAttr("shipBonusCarrierA4"), skill="Amarr Carrier")
