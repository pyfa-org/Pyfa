# shipBonusCarrierM3FighterVelocity
#
# Used by:
# Ship: Nidhoggur
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity", src.getModifiedItemAttr("shipBonusCarrierM3"), skill="Minmatar Carrier")
