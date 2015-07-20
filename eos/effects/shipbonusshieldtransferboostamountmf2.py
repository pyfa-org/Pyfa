# shipBonusShieldTransferBoostAmountMF2
#
# Used by:
# Ship: Burst
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
