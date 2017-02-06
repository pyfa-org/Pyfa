# shipShieldTransferFalloffMC2
#
# Used by:
# Ship: Scimitar
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "falloffEffectiveness",
                                  src.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
