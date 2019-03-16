# shipBonusShieldBoostAmountMC2
#
# Used by:
# Ship: Vagabond
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
