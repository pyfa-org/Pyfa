# shipBonusForceAuxiliaryM2LocalBoostAmount
#
# Used by:
# Ship: Lif
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"), "shieldBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryM2"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"), "shieldBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryM2"), skill="Minmatar Carrier")
