type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Warfare Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Siege Warfare Specialist"), "commandBonus", src.getModifiedItemAttr("shipBonusCarrierM4"), skill="Minmatar Carrier")
