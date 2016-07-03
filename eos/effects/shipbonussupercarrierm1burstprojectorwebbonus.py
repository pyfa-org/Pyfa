# shipBonusSupercarrierM1BurstProjectorWebBonus
#
# Used by:
# Ship: Hel
# Ship: Vendetta
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Burst Projector Operation"), "speedFactor", src.getModifiedItemAttr("shipBonusSupercarrierM1"), skill="Minmatar Carrier")
