type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"), "falloffEffectiveness", src.getModifiedItemAttr("carrierCaldariBonus3"), skill="Caldari Carrier")
