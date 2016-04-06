# shipBonusForceAuxiliaryC4WarfareLinksBonus
#
# Used by:
# Ship: Minokawa
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Siege Warfare Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryC4"), skill="Caldari Carrier")
