# shipBonusShieldTransferBoostAmountCF2
#
# Used by:
# Variations of ship: Bantam (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
