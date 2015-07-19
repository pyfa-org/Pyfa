# shipBonusShieldBoostMI2
#
# Used by:
# Ship: Mastodon
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMI2"), skill="Minmatar Industrial")
