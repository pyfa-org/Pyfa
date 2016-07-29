# shipBonusSupercarrierM2FighterVelocity
#
# Used by:
# Ship: Hel
# Ship: Vendetta
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity", src.getModifiedItemAttr("shipBonusSupercarrierM2"), skill="Minmatar Carrier")
