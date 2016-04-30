# shipBonusCarrierA2SupportFighterBonus
#
# Used by:
# Ship: Archon
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterSquadronOrbitRange", src.getModifiedItemAttr("shipBonusCarrierA2"), skill="Amarr Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterAbilityEnergyNeutralizerOptimalRange", src.getModifiedItemAttr("shipBonusCarrierA2"), skill="Amarr Carrier")
