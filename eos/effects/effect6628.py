# shipBonusCarrierM2SupportFighterBonus
#
# Used by:
# Ship: Nidhoggur
type = "passive"


def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterSquadronOrbitRange",
                                   src.getModifiedItemAttr("shipBonusCarrierM2"), skill="Minmatar Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"),
                                   "fighterAbilityStasisWebifierOptimalRange",
                                   src.getModifiedItemAttr("shipBonusCarrierM2"), skill="Minmatar Carrier")
