# shipBonusCarrierG2SupportFighterBonus
#
# Used by:
# Ship: Thanatos
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterSquadronOrbitRange", src.getModifiedItemAttr("shipBonusCarrierG2"), skill="Gallente Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterAbilityWarpDisruptionRange", src.getModifiedItemAttr("shipBonusCarrierG2"), skill="Gallente Carrier")
