# shipBonusCarrierC2SupportFighterBonus
#
# Used by:
# Ship: Chimera
type = "passive"


def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"), "fighterSquadronOrbitRange",
                                   src.getModifiedItemAttr("shipBonusCarrierC2"), skill="Caldari Carrier")
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Support Fighters"),
                                   "fighterAbilityECMRangeOptimal", src.getModifiedItemAttr("shipBonusCarrierC2"),
                                   skill="Caldari Carrier")
