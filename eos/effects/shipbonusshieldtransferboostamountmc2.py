# shipBonusShieldTransferBoostAmountMC2
#
# Used by:
# Ship: Scythe
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
