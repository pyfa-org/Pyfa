# shipBonusSupercarrierG2FighterHitpoints
#
# Used by:
# Variations of ship: Nyx (2 of 2)
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity", src.getModifiedItemAttr("shipBonusSupercarrierG2"), skill="Gallente Carrier")
