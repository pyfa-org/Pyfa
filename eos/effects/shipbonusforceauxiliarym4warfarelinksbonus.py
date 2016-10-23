# shipBonusForceAuxiliaryM4WarfareLinksBonus
#
# Used by:
# Ship: Lif
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryM4"), skill="Minmatar Carrier")
