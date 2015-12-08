# carrierCaldariShieldTransferFalloff3
#
# Used by:
# Ship: Chimera
# Ship: Revenant
# Ship: Wyvern
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"), "falloffEffectiveness", src.getModifiedItemAttr("carrierCaldariBonus3"), skill="Caldari Carrier")
