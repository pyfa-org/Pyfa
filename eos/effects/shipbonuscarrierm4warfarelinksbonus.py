# shipBonusCarrierM4WarfareLinksBonus
#
# Used by:
# Ship: Nidhoggur
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")
