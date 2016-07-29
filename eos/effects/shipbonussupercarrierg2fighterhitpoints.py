# shipBonusSupercarrierG2FighterHitpoints
#
# Used by:
# Ship: Nyx
# Ship: Vendetta
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity", src.getModifiedItemAttr("shipBonusSupercarrierG2"), skill="Gallente Carrier")
