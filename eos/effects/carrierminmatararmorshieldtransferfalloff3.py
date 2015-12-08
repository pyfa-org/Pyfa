# carrierMinmatarArmor&ShieldTransferFalloff3
#
# Used by:
# Ship: Hel
# Ship: Nidhoggur
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems") or mod.item.requiresSkill("Capital Remote Armor Repair Systems"), "falloffEffectiveness", src.getModifiedItemAttr("carrierMinmatarBonus3"), skill="Minmatar Carrier")
