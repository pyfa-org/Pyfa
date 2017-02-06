# shipShieldTransferFalloffCC1
#
# Used by:
# Ship: Basilisk
# Ship: Etana
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "falloffEffectiveness",
                                  src.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")
