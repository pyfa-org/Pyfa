# shipBonusShieldTransferBoostAmountCF2
#
# Used by:
# Ship: Bantam
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
