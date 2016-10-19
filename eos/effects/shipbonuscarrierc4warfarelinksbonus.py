# shipBonusCarrierC4WarfareLinksBonus
#
# Used by:
# Ship: Chimera
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Siege Warfare Specialist"), "commandBonus",
                                  src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"), "commandBonus",
                                  src.getModifiedItemAttr("shipBonusCarrierC4"), skill="Caldari Carrier")
