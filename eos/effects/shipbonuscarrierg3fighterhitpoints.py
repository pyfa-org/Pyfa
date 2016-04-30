# shipBonusCarrierG3FighterHitpoints
#
# Used by:
# Ship: Thanatos
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity", src.getModifiedItemAttr("shipBonusCarrierG3"), skill="Gallente Carrier")
